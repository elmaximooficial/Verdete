$net = Get-WmiObject Win32_NetworkAdapterConfiguration | Where-Object {$_.IPEnabled -eq $true} | Select DefaultIPGateway, Description, DHCPEnabled, DHCPServer, DNSServerSearchOrder, DHCPLeaseExpires, DHCPLeaseObtained, IPAddress, Index, InterfaceIndex, MACAddress
$printers = Get-WmiObject Win32_Printer | Select Name, PortName, DriverName, Default, AveragePagesPerMinute, CapabilityDescription, Caption, DeviceID, Network, PrinterState, PrinterStatus, Priority, Servername, SpoolEnabled, Status, StatusInfo
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