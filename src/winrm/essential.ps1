$processor = Get-WmiObject Win32_Processor | Select Architecture, Caption, Description, Manufacturer, Name, NumberOfCores, NumberOfLogicalProcessors, SerialNumber, ProcessorId
$os = Get-WmiObject Win32_OperatingSystem | Select BootDevice, BuildNumber, BuildType, Caption, CountryCode, Description, InstallDate, LastBootUpTime, LocalDateTime, Organization, OSArchitecture, SerialNumber, RegisteredUser, Version, SystemDrive
$net = Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $true} | Select DefaultIPGateway, Description, DHCPEnabled, DHCPServer, DNSServerSearchOrder, DHCPLeaseExpires, DHCPLeaseObtained, IPAddress, Index, InterfaceIndex, MACAddress
$printers = Get-WmiObject Win32_Printer | Select Name, PortName, DriverName, Default, AveragePagesPerMinute, CapabilityDescription, Caption, DeviceID, Network, PrinterState, PrinterStatus, Priority, Servername, SpoolEnabled, Status, StatusInfo
$computer = Get-WmiObject WIn32_ComputerSystem | Select AdminPasswordStatus, BootStatus, BootupState, ChassisSKUNumber, CurrentTimeZone, OEMStringArray, PrimaryOwnerName, SystemFamily, Manufacturer, Model, SystemSKUNumber, TotalPhysicalMemory, UserName
@"
	{
		"cpu_architecture": $($processor.architecture),
		"cpu_caption": "$($processor.caption)",
		"cpu_description": "$($processor.description)",
		"cpu_manufacturer": "$($processor.manufacturer)",
		"cpu_name": "$($processor.name)",
		"cpu_cores": $($processor.numberofcores),
		"cpu_nolp": $($processor.numberoflogicalprocessors),
		"cpu_serial": "$($processor.serialnumber)",
		"cpu_processor_id": "$($processor.processorid)",
		"os_build_number": $($os.buildnumber),
		"os_build_type": "$($os.buildtype)",
		"os_caption": "$($os.caption)",
		"os_country_code": $($os.countrycode),
		"os_description": "$($os.description)",
		"os_install_date": "$($os.installdate)",
		"os_last_boot_up_time": "$($os.lastbootuptime)",
		"os_local_time": "$($os.localdatetime)",
		"os_organization": "$($os.organization)",
		"os_architecture": "$($os.osarchitecture)",
		"os_serial": "$($os.serialnumber)",
		"os_registerd_user": "$($os.registereduser)",
		"os_version": "$($os.version)",
		"os_system_drive": "$($os.systemdrive)",
		"computer_admin_password_state": $($computer.adminpasswordstatus),
		"computer_boot_status": [$(($computer.bootstatus -join ','))],
		"computer_boot_up_state": "$($computer.bootupstate)",
		"computer_chassis_sku_number": "$($computer.chassisskunumber)",
		"computer_current_time_zone": $($computer.currenttimezone),
		"computer_oem_string_array": ["$(($computer.oemstringarray -join '","'))"],
		"computer_primary_owner_name": "$($computer.primaryownername)",
		"computer_system_family": "$($computer.systemfamily)",
		"computer_manufacturer": "$($computer.manufacturer)",
		"computer_model": "$($computer.model)",
		"computer_system_sku_number": "$($computer.systemskunumber)",
		"computer_total_physical_memory": $($computer.totalphysicalmemory),
		"computer_user_name": "$($computer.username.replace('PA\', 'PA\\'))",
		"net_interfaces": [$($net_formatted = New-Object System.Collections.Generic.List[System.Object];foreach($interface in $net){
		$net_formatted.Add("
		{
			`"default_gateway`": `"$($interface.defaultipgateway)`",
			`"description`": `"$($interface.description)`",
			`"dhcp_enabled`": $(($interface.dhcpenabled | Out-String).tolower()),
			`"dhcp_server`": `"$($interface.dhcpserver)`",
			`"dns_server_search_order`": [`"$(($interface.dnsserversearchorder -join '","'))`"],
			`"dhcp_lease_expires`": `"$($interface.dhcpleaseexpires)`",
			`"dhcp_lease_obtained`": `"$($interface.dhcpleaseobtained)`",
			`"ip_addresses`": [`"$(($interface.ipaddress -join '","'))`"],
			`"index`": $($interface.index),
			`"interface_index`": $($interface.interfaceindex),
			`"mac_address`": `"$($interface.macaddress)`"
		}
		")
		}($net_formatted -join ','))],
		"printers": [$($printers_formatted = New-Object System.Collections.Generic.List[System.Object];foreach($printer in $printers){
		$printers_formatted.add("
		{
			`"name`": `"$(($printer.name).replace(`"\`", `"\\`"))`",
			`"port_name`": `"$($printer.portname)`",
			`"driver_name`": `"$($printer.drivername)`",
			`"default`": $(($printer.default | Out-String).tolower()),
			`"average_pages_per_minute`": $($printer.averagepagesperminute),
			`"capability_description`": [`"$(($printer.capabilitydescription -join '","'))`"],
			`"caption`": `"$(($printer.caption).replace(`"\`", `"\\`"))`",
			`"device_id`": `"$(($printer.deviceid).replace(`"\`", `"\\`"))`",
			`"network`": $(($printer.network | Out-String).tolower()),
			`"printer_state`": `"$($printer.state)`",
			`"printer_status`": `"$($printer.status)`",
			`"printer_status_info`": `"$($printer.statusinfo)`"
		}")
		} ($printers_formatted -join ','))]
	}
"@