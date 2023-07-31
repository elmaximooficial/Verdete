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
    computer_admin_password_status: int
    computer_boot_status: str
    computer_boot_up_state: list[int]
    computer_chassis_sku_number: str
    computer_current_time_zone: int
    computer_oem_string_array: list[str]
    computer_primary_owner_name: str
    computer_system_family: str
    computer_manufacturer: str
    computer_model: str
    computer_system_sku_number: str
    computer_total_physical_memory: int
    computer_user_name: str

class Disk(NamedTuple):
    disk_caption: str
    disk_compression_method: str
    disk_description: str
    disk_default_block_size: int
    disk_firmware_revision: str
    disk_index: int
    disk_interface_type: str
    disk_manufacturer: str
    disk_model: str
    disk_serial: str
    disk_size: int
    disk_status: str
    disk_status_info: str
    disk_total_cylinders: int
    disk_total_heads: int
    disk_total_sectors: int
    disk_total_tracks: int

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
    mobo_status: str
    mobo_weight: int
    mobo_width: int
    mobo_slot_layout: str
    software_caption: str
    software_description: str
    software_id: str
    software_install_date: datetime.date
    software_last_use: datetime.date
    software_product_name: str
    software_vendor: str
    software_version: str
    disk: list[Disk]
    gpu_accelerator_capabilities: list[str]
    gpu_adapter_compatibility: str
    gpu_adapter_dac_type: str
    gpu_adapter_ram: str
    gpu_caption: str
    gpu_color_table_entries: list[str]
    gpu_current_refresh_rate: int
    gpu_description: str
    gpu_driver_date: datetime.date
    gpu_driver_version: str
    gpu_inf_file_name: str
    gpu_inf_section: str
    gpu_install_date: datetime.date
    gpu_last_error_code: int
    gpu_status: str
    gpu_status_info: str

class Monitor(NamedTuple):
    caption: str
    description: str
    manufacturer: str
    type: str
    name: str
    pixels_per_logical_x_inch: int
    pixels_per_logical_y_inch: int
    screen_height: int
    screen_width: int
    status: str
    status_info: str

class Product(NamedTuple):
    product_caption: str
    product_description: str
    product_id: str
    product_install_date: datetime.date
    product_install_source: str
    product_local_package: str
    product_name: str
    product_package_name: str
    product_package_id: str
    product_sku: str
    product_version: str
    product_vendor: str

class Tertiary(BaseModel):
    bios_characteristics: list[int]
    bios_version: str
    bios_build_number: str
    bios_caption: str
    bios_current_language: str
    bios_description: str
    bios_install_date: datetime.date
    bios_manufacturer: str
    bios_name: str
    bios_serial: str
    bios_release_date: datetime.date
    monitor: list[Monitor]
    keyboard_caption: str
    keyboard_description: str
    keyboard_name: str
    keyboard_status: str
    keyboard_status_info: str
    mouse_caption: str
    mouse_description: str
    mouse_hardware_type: str
    mouse_inf_file_name: str
    mouse_inf_section: str
    mouse_manufacturer: str
    mouse_name: str
    mouse_number_of_buttons: str
    mouse_pointing_type: str
    mouse_status: str
    mouse_status_info: str
    products: list[Product]

class Service(NamedTuple):
    caption: str
    check_point: str
    description: str
    display_name: str
    install_date: datetime.date
    path_name: str
    name: str
    process_id: int
    started: bool
    start_mode: str
    start_name: str
    status: str
    status_info: str

class Share(NamedTuple):
    caption: str
    description: str
    install_date: datetime.date
    maximum_allowed: int
    name: str
    path: str
    status: str
    type: str

class NonEssential(BaseModel):
    kb_caption: str
    kb_description: str
    kb_comments: str
    kb_id: str
    kb_install_date: datetime.date
    kb_name: str
    kb_status: str
    kb_installed_by: str
    services: list[Service]
    shares: list[Share]

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
