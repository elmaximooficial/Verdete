import datetime

from src.winrm.windows import WINRM_TRANSPORT, WINRM_PROTOCOL, WinRMConnection
from src.winrm.host_group import HostGroup
from src.winrm.task_group import WinRMTask
from pydantic import BaseModel
from typing import NamedTuple

class NetInterface(NamedTuple):
    default_gateway: str
    description: str
    dhcp_enabled: bool
    dhcp_server: str
    dns_server_search_order: list[str]
    dhcp_lease_expires: int
    dhcp_lease_obtained: int
    ip_address: str
    index: int
    interface_index: int
    mac_address: str

class Printer(NamedTuple):
    name: str
    port_name: str
    driver_name: str
    default: bool
    average_pages_per_minute: int
    capability_description: list[str]
    caption: str
    device_id: str
    network: bool
    printer_state: str
    printer_status: str
    priority: int
    server_name: str
    spooler_name: str
    status: str
    status_info: str

class Essential(BaseModel):
    cpu_architecture: str
    cpu_caption: str
    cpu_description: str
    cpu_manufacturer: str
    cpu_name: str
    cpu_cores: int
    cpu_nolp: int
    cpu_serial: str
    cpu_processor_id: str
    os_boot_device: str
    os_build_number: int
    os_build_type: str
    os_caption: str
    os_country_code: int
    os_description: str
    os_install_date: datetime.date
    os_last_boot_up: datetime.date
    os_local_time: datetime.date
    os_organization: str
    os_architecture: str
    os_serial: str
    os_registered_user: str
    os_version: str
    os_system_drive: str
    net_interfaces: list[NetInterface]
    printers: list[Printer]
    computer_admin_password_state: int
    computer_boot_status: str
    computer_boot_up_state: str
    computer_chassis_sku_number: str
    computer_current_time_zone: str
    computer_oem_string_array: list[str]
    computer_primary_owner_name: str
    computer_system_family: str
    computer_manufacturer: str
    computer_model: str
    computer_system_sku_number: str
    computer_total_physical_memory: int
    computer_user_name: str

class Secondary(BaseModel):
    mem_capacity: int
    mem_caption: str
    mem_configured_clock: int
    mem_configured_voltage: int
    mem_data_width: str
    mem_description: str
    mem_device_location: str
    mem_form_factor: str
    mem_manufacturer: str
    mem_part_number: str
    mem_serial_number: str
    mem_speed: int
    mobo_description: str
    mobo_height: int
    mobo_hosting_board: str
    mobo_install_date: datetime.date
    mobo_manufacturer: str
    mobo_name: str
    mobo_model: str
    mobo_part_number: str
    mobo_product: str
    mobo_serial: str
    mobo_sku: str
    mobo_version: str

class WMITaskGroup:
    tasks = [{'name': 'Essential',
              'tasks': WinRMConnection.encode_command(
                  r'$processor = Get-WmiObject Win32_Processor | Select Architecture, Caption, Description, Manufacturer, Name, NumberOfCores, NumberOfLogicalProcessors, SerialNumber, ProcessorsId' +
                  r'$os = Get-WmiObject Win32_OperatingSystem | Select BootDevice, BuildNumber, BuildType, Caption, CountryCode, Description, InstallDate, LastBootUpTime, LocalDateTime, Organization, OSArchitecture, SerialNumber, RegisteredUser, Version, SystemDrive' +
                  r'$net = Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $True} | Select DefaultIPGateway, Description, DHCPEnabled, DHCPServer, DNSServerSearchOrder, DHCPLeaseExpires, DHCPLeaseObtained, IPAddress, Index, InterfaceIndex, MACAddress' +
                  r'$printer = Get-WmiObject Win32_Printer | Select Name, PortName, DriverName, Default, AveragePagesPerMinute, CapabilityDescription, Caption, DeviceID, Network, PrinterState, PrinterStatus, Priority, ServerName, SpoolEnabled, Status, StatusInfo' +
                  r'$computer = Get-WmiObject Win32_ComputerSystem | Select AdminPasswordStates, BootStatus, BootupState, ChassisSKUNumber, CurrentTimeZone, OEMStringArray, PrimaryOwnerName, SystemFamily, Manufacturer, Model, SystemSKUNumber, TotalPhysicalMemory, UserName')},
             {'name': "Secondary",
              'tasks': WinRMConnection.encode_command(
                  r'$mem = Get-WmiObject Win32_PhysicalMemory | Select Capacity, Caption, ConfiguredClockSpeed, ConfiguredVoltage, DataWidth, Description, DeviceLocator, FormFactor, Manufacturer, PartNumber, SerialNumber, Speed' +
                  r'$mobo = Get-WmiObject Win32_BaseBoard | Select Description, Height, HostingBoard, InstallDate, Manufacturer, Name, Model, PartNumber, Product, SerialNumber, SKU, Version, Status, Weight, Width, SlotLayout' +
                  r'$software = Get-WmiObject Win32_SoftwareFeature | Select Caption, Description, IdentifyingNumber, InstallDate, LastUse, ProductName, Vendor, Version' +
                  r'$disk = Get-WmiObject Win32_DiskDrive | Select Caption, CompressionMethod, Description, DefaultBlockSize, FirmwareRevision, Index, InterfaceType, Manufacturer, Model, SerialNumber, Size, Status, StatusInfo, TotalCylinders, TotalHeads, TotalSectors, TotalTracks' +
                  r'$gpu = Get-WmiObject Win32_VideoController | Select AcceleratorCapabilities, AdapterCompatibility, AdapterDACType, AdapterRAM, Caption, ColoTableEntries, CurrentRefreshRate, Description, DriverDate, DriverVersion, InfFilename, InfSection, InstallDate, LastErrorCode, Status, StatusInfo')},
             {'name': "Tertiary",
              'tasks': WinRMConnection.encode_command(
                  r'$bios = Get-WmiObject Win32_BIOS | Select BiosCharacteristics, BIOSVersion, BuildNumber, Caption, CurrentLanguage, Description, InstallDate, Manufacturer, Name, SerialNumber, ReleaseDate' +
                  r'$monitor = Get-WmiObject Win32_DesktopMonitor | Select Caption, Description, MonitorManufacturer, MonitorType, Name, PixelsPerLogicalXInch, PixelsPerLogicalYInch, ScreenHeight, ScreenWidth, Status, StatusInfo' +
                  r'$keyboard = Get-WmiObject Win32_Keyboard | Select Caption, Description, Name, Status, StatusInfo' +
                  r'$mouse = Get-WmiObject Win32_PointingDevice | Select Caption, Description, HardwareType, InfFileName, InfSection, Manufacturer, Name, NumberOfButtons, PointingType, Status, StatusInfo' +
                  r'$product = Get-WmiObject Win32_Product | Select Caption, Description, IdentifyingNumber, InstallDate, InstallSource, LocalPackage, Name, PackageName, ProductID, SKUNumber, Version, Vendor')},
             {'name': 'Non-Essential',
              'tasks': WinRMConnection.encode_command(
                  r'$kb = Get-WmiObject Win32_QuickFixEngineering | Select Caption, Description, FixComments, HotFixID, InstallDate, Name, Status, InstalledBy' +
                  r'$service = Get-WmiObject Win32_Service | Select Caption, CheckPoint, Description, DisplayName, InstallDate, PathName, Name, ProcessId, Started, StartMode, StartName, State, Status' +
                  r'$share = Get-WmiObject Win32_Share | Select Caption, Description, InstallDate, MaximumAllowed, Name, Path, Status, Type')}]
    async def execute(self):
