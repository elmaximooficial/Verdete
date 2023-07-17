import asyncio
import sys, getopt
from src.winrm.windows import WINRM_TRANSPORT
from src.util.ldap import LDAP
from src.winrm.task import Task, FAILURE_ACTION
from src.winrm.task_group import TaskGroup
from src.winrm.host import Host
from src.util.password_manager import PasswordManager, User
from src.winrm.host_group import HostGroup
from src.database.db_handler import DBHandler
from getpass import getpass
import json

########## Configuration file format ##########
#### [ldap]                              
#### server = address_to_server
#### port = port_for_server (optional, default=389)
#### base_dn = root dn for searching computers
#### use_ssl = Allow for ssl
#### user = User for connection to the database
#### domain = User domain name
#### [mongodb]
#### server = address_to_server
#### port = server_port
#### user = server's user
#### password = password
#### database = database

def hostname_check(result : dict):
    print(result["Results"]["OS"]["Hostname"])
    return result["Results"]["OS"]["Hostname"] == "PM-NOTEINFO99"

class Main:
    async def main(self, argv):
        opts, args = getopt.getopt(argv, '', ['fetch-computers', 'gen-password=', 'gen-key', 'query-computers'])
        for i, arg in opts:
            if i in ['--gen-password']:
                pass_manager = PasswordManager.load_key()
                username, password = arg.split('~')
                pass_manager.gen_encrypted_pwd(username=username, password=password)
            if i in ['--gen-key']:
                PasswordManager.gen_key()
            if i in ['--fetch-computers']:
                ldap_conn = LDAP()
                await ldap_conn.connect_to_server()
                async for i in ldap_conn.fetch_computers():
                    print(i)
                await ldap_conn.dispose_connection()
            if i in ['--query-computers']:
                ldap_conn = LDAP()
                await ldap_conn.connect_to_server()
                
                username = input('Insert the Username: ')
                password = getpass('Insert the Password: ')
                
                user = User(username, password)
                
                wmi_check = lambda x: x != None
                cpu_task = Task(name="CPU", 
                #            pre_check=r' " """Hostname`t$(hostname)""" "', 
                #            pre_checking=wmi_check, 
                #            pre_check_failure_action=FAILURE_ACTION.STOP_EXECUTION,
                            script= r'Get-WmiObject Win32_Processor | Select Architecture, Caption, Description, Manufacturer, Name, NumberOfCores, NumberOfLogicalProcessors, SerialNumber, ProcessorsId | ConvertTo-Csv', 
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
                            os_task,
                            net_task,
                            computer_task,
                            printer_task,
                            physical_memory_task,
                            base_board_task,
                            software_feature_task,
                            disk_drive_task,
                            video_controller_task,
                            bios_task,
                            desktop_monitor_task,
                            keyboard_task,
                            pointing_device_task,
                            product_task,
                            quickfix_engineering_task,
                            service_task,
                            share_task,
                            transport=WINRM_TRANSPORT.NTLM)
                
                computers = ['PM-CPDADM001', 'PM-CPDADM002', 'PM-CPDADM003', 'PM-CPDADM004', 'PM-SAFCPD007', 'ADM002', 'PM-NOTEINFO99']
                
                host_group = HostGroup(Host("PM-CPDADM001"), Host("PM-CPDADM002"), Host("PM-CPDADM004"), Host("PM-SAFCPD007"), Host("ADM002"), Host("PM-NOTEINFO99"), name="CPD", description="Computers from ITD")
                
                
                available = HostGroup(name="Available", description="All Computers Available")
                #for i in computers:
                #    async for j in os_task.execute(Host(i), user):
                #        print(j)
                
                #async for i in task_group.execute(group=host_group, user=user):
                #    print(i)
                #    if json.loads(i)["Status"] == "Success":
                #        available.hosts.append(Host(json.loads(i)["Hostname"])
                    
                db_handler = DBHandler()
                collection = db_handler.connect(collection='hosts')
                async for i in ldap_conn.fetch_computers():
                    async for j in task_group.execute(host=Host(i), user=user, db_handler=db_handler, collection=collection, debug=False):
                        print(j)
if __name__ == '__main__':
    main = Main()
    asyncio.run(main.main(sys.argv[1:]))