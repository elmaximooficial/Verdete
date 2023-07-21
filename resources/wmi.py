import src.winrm.windows
from src.winrm.task import Task, FAILURE_ACTION, WINRM_TRANSPORT
from src.winrm.task_group import TaskGroup

wmi_check = lambda x: x != None

cpu_task = Task(name="CPU",
                #            pre_check=r' " """Hostname`t$(hostname)""" "',
                #            pre_checking=wmi_check,
                #            pre_check_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                script=r'Get-WmiObject Win32_Processor | Select Architecture, Caption, Description, Manufacturer, Name, NumberOfCores, NumberOfLogicalProcessors, SerialNumber, ProcessorsId | ConvertTo-Csv',
                script_checking=wmi_check,
                script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                transport=WINRM_TRANSPORT.NTLM)
os_task = Task(name="OS",
               #            pre_check=r' " """Hostname`t$($hostname)""" "',
               #            pre_checking=hostname_check,
               #            pre_check_failure_action=FAILURE_ACTION.ALTERNATIVE_TASK,
               #            pre_check_alternative=cpu_task,
               script='Get-WmiObject Win32_OperatingSystem | Select BootDevice, BuildNumber, BuildType, Caption, CountryCode, Description, InstallDate, LastBootUpTime, LocalDateTime, Organization, OSArchitecture, SerialNumber, RegisteredUser, Version, SystemDrive | ConvertTo-Csv',
               script_checking=wmi_check,
               script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
               transport=WINRM_TRANSPORT.NTLM)
net_task = Task(name="Networking",
                script='Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $True} | Select DefaultIPGateway, Description, DHCPEnabled, DHCPServer, DNSServerSearchOrder, DHCPLeaseExpires, DHCPLeaseObtained, IPAddress, Index, InterfaceIndex, MACAddress | ConvertTo-Csv',
                script_checking=wmi_check,
                script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                transport=WINRM_TRANSPORT.NTLM)
printer_task = Task(name="Printer",
                    script='Get-WmiObject Win32_Printer | Select Name, PortName, DriverName, Default, AveragePagesPerMinute, CapabilityDescription, Caption, DeviceID, Network, PrinterState, PrinterStatus, Priority, ServerName, SpoolEnabled, Status, StatusInfo | ConvertTo-Csv',
                    script_checking=wmi_check,
                    script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                    transport=WINRM_TRANSPORT.NTLM)

computer_task = Task(name="Computer",
                     script='Get-WmiObject Win32_ComputerSystem | Select AdminPasswordStates, BootStatus, BootupState, ChassisSKUNumber, CurrentTimeZone, OEMStringArray, PrimaryOwnerName, SystemFamily, Manufacturer, Model, SystemSKUNumber, TotalPhysicalMemory, UserName | ConvertTo-Csv',
                     script_checking=wmi_check,
                     script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                     transport=WINRM_TRANSPORT.NTLM
                     )
physical_memory_task = Task(name="PhysicalMemory",
                            script='Get-WmiObject Win32_PhysicalMemory | Select Capacity, Caption, ConfiguredClockSpeed, ConfiguredVoltage, DataWidth, Description, DeviceLocator, FormFactor, Manufacturer, PartNumber, SerialNumber, Speed | ConvertTo-Csv',
                            script_checking=wmi_check,
                            script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                            transport=WINRM_TRANSPORT.NTLM)
base_board_task = Task(name="BaseBoard",
                       script='Get-WmiObject Win32_BaseBoard | Select Description, Height, HostingBoard, InstallDate, Manufacturer, Name, Model, PartNumber, Product, SerialNumber, SKU, Version, Status, Weight, Width, SlotLayout | ConvertTo-Csv',
                       script_checking=wmi_check,
                       script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                       transport=WINRM_TRANSPORT.NTLM)
software_feature_task = Task(name="SoftwareFeature",
                             script='Get-WmiObject Win32_SoftwareFeature | Select Caption, Description, IdentifyingNumber, InstallDate, LastUse, ProductName, Vendor, Version | ConvertTo-Csv',
                             script_checking=wmi_check,
                             script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                             transport=WINRM_TRANSPORT.NTLM)
disk_drive_task = Task(name="DiskDrive",
                       script='Get-WmiObject Win32_DiskDrive | Select Caption, CompressionMethod, Description, DefaultBlockSize, FirmwareRevision, Index, InterfaceType, Manufacturer, Model, SerialNumber, Size, Status, StatusInfo, TotalCylinders, TotalHeads, TotalSectors, TotalTracks | ConvertTo-Csv',
                       script_checking=wmi_check,
                       script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                       transport=WINRM_TRANSPORT.NTLM)
video_controller_task = Task(name="VideoController",
                             script='Get-WmiObject Win32_VideoController | Select AcceleratorCapabilities, AdapterCompatibility, AdapterDACType, AdapterRAM, Caption, ColoTableEntries, CurrentRefreshRate, Description, DriverDate, DriverVersion, InfFilename, InfSection, InstallDate, LastErrorCode, Status, StatusInfo | ConvertTo-Csv',
                             script_checking=wmi_check,
                             script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                             transport=WINRM_TRANSPORT.NTLM)
bios_task = Task(name="BIOS",
                 script='Get-WmiObject Win32_BIOS | Select BiosCharacteristics, BIOSVersion, BuildNumber, Caption, CurrentLanguage, Description, InstallDate, Manufacturer, Name, SerialNumber, ReleaseDate | ConvertTo-Csv',
                 script_checking=wmi_check,
                 script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                 transport=WINRM_TRANSPORT.NTLM)
desktop_monitor_task = Task(name="DesktopMonitor",
                            script='Get-WmiObject Win32_DesktopMonitor | Select Caption, Description, MonitorManufacturer, MonitorType, Name, PixelsPerLogicalXInch, PixelsPerLogicalYInch, ScreenHeight, ScreenWidth, Status, StatusInfo | ConvertTo-Csv',
                            script_checking=wmi_check,
                            script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                            transport=WINRM_TRANSPORT.NTLM)
keyboard_task = Task(name="Keyboard",
                     script='Get-WmiObject Win32_Keyboard | Select Caption, Description, Name, Status, StatusInfo | ConvertTo-Csv',
                     script_checking=wmi_check,
                     script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                     transport=WINRM_TRANSPORT.NTLM)
pointing_device_task = Task(name="PointingDevice",
                            script='Get-WmiObject Win32_PointingDevice | Select Caption, Description, HardwareType, InfFileName, InfSection, Manufacturer, Name, NumberOfButtons, PointingType, Status, StatusInfo | ConvertTo-Csv',
                            script_checking=wmi_check,
                            script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                            transport=WINRM_TRANSPORT.NTLM)
product_task = Task(name="Product",
                    script='Get-WmiObject Win32_Product | Select Caption, Description, IdentifyingNumber, InstallDate, InstallSource, LocalPackage, Name, PackageName, ProductID, SKUNumber, Version, Vendor | ConvertTo-Csv',
                    script_checking=wmi_check,
                    script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                    transport=WINRM_TRANSPORT.NTLM)
quickfix_engineering_task = Task(name="QuickFixEngineering",
                                 script='Get-WmiObject Win32_QuickFixEngineering | Select Caption, Description, FixComments, HotFixID, InstallDate, Name, Status, InstalledBy | ConvertTo-Csv',
                                 script_checking=wmi_check,
                                 script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                                 transport=WINRM_TRANSPORT.NTLM
                                 )
service_task = Task(name="Service",
                    script='Get-WmiObject Win32_Service | Select Caption, CheckPoint, Description, DisplayName, InstallDate, PathName, Name, ProcessId, Started, StartMode, StartName, State, Status | ConvertTo-Csv',
                    script_checking=wmi_check,
                    script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                    transport=WINRM_TRANSPORT.NTLM
                    )
share_task = Task(name="Share",
                  script='Get-WmiObject Win32_Share | Select Caption, Description, InstallDate, MaximumAllowed, Name, Path, Status, Type | ConvertTo-Csv',
                  script_checking=wmi_check,
                  script_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                  transport=WINRM_TRANSPORT.NTLM
                  )

task_group = TaskGroup(
    cpu_task,
    transport=WINRM_TRANSPORT.NTLM)
