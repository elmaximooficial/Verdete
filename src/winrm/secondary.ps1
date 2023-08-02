$mems = Get-WMiObject WIn32_PhysicalMemory | Select-Object Capacity, Caption, COnfiguredClockSpeed, ConfiguredVoltage, DataWidth, Description, DeviceLocator, FormFactor, Manufacturer, PartNumber, SerialNumber, Speed
$mobo = Get-WMiObject Win32_BaseBoard | Select-Object Description, Height, HostingBoard, InstallDate, Manufacturer, Name, Model, PartNumber, Product, SerialNumber, SKU, Version, Status, Weight, Width, SlotLayout
$softwares = Get-WMiObject Win32_SoftwareFeature | Select-Object Caption, Description, IdentifyingNumber, InstallDate, LastUse, ProductName, Vendor, Version
$disks = Get-WmiObject Win32_DiskDrive | Select-Object Caption, CompressionMethod, Description, DefaultBlockSize, FirmwareRevision, Index, INterfaceType, Manufacturer, Model, SerialNumber, Size, Status, StatusInfo, TotalCylinders, TotalHeads, TotalSectors, TOtalTracks
$gpu = Get-WmiObject WIn32_VideoController | Select-Object AcceleratorCapabilites, AdapterCompatibility, AdapterDACType, AdapterRAM, Caption, ColorTableEntires, CurrentRefreshRate, Description, DriverDate, DriverVersion, InfFilename, InfSection, InstallDate, LastErrorCode, Status, StatusInfo
@"
{
	"mems": [$($mems_formatted = New-Object System.Collections.Generic.List[System.Object];Foreach($mem in $mems){
	$mems_formatted.Add("
	{
		`"mem_capacity`": $($mem.capacity),
		`"mem_caption`": `"$($mem.caption)`",
		`"mem_configured_clock`": $($mem.configuredclockspeed),
		`"mem_configured_voltage`": $($mem.configuredvoltage),
		`"mem_data_width`": $($mem.datawidth),
		`"mem_description`": `"$($mem.description)`",
		`"mem_device_locator`": `"$($mem.devicelocator)`",
		`"mem_form_factor`": `"$($mem.formfactor)`",
		`"mem_manufacturer`": `"$($mem.maunfacturer)`",
		`"mem_part_number`": `"$($mem.serialnumber)`",
		`"mem_speed`": $($mem.speed)
	}
	")
	}$mems_formatted -join ',')],
	"mobo_description": "$($mobo.description)",
	"mobo_height": "$($mobo.height)",
	"mobo_hosting_board": "$($mobo.hostingboard)",
	"mobo_install_date": "$($mobo.installdate)",
	"mobo_manufacturer": "$($mobo.manufacturer)",
	"mobo_name": "$($mobo.name)",
	"mobo_model": "$($mobo.model)",
	"mobo_part_number": "$($mobo.partnumber)",
	"mobo_product": "$($mobo.product)",
	"mobo_serial": "$($mobo.serialnumber)",
	"mobo_sku": "$($mobo.sku)",
	"mobo_version": "$($mobo.version)",
	"mobo_status": "$($mobo.status)",
	"mobo_weight": "$($mobo.weight)",
	"mobo_width": "$($mobo.width)",
	"mobo_slot_layout": "$($mobo.slotlayout)",
	"softwares": [$($softwares_formatted = New-Object System.Collections.Generic.List[System.Object];Foreach($software in $softwares){
	$softwares_formatted.Add("
	{
		`"software_caption`": `"$($software.caption)`",
		`"software_description`": `"$($software.description)`",
		`"software_id`": `"$($software.identifyingnumber)`",
		`"software_install_date`": `"$($software.installdate)`",
		`"software_last_use`": `"$($software.lastuse)`",
		`"software_product_name`": `"$($software.productname)`",
		`"software_vendor`": `"$($software.vendor)`",
		`"software_version`": `"$($software.version)`"
	}")
	} ($softwares_formatted -join ','))],
	"gpu_accelerator_capabilities": ["$(($gpu.acceleratorcapabilities -join '","'))"],
	"gpu_adapter_compatibility": "$($gpu.adaptercompatibility)",
	"gpu_adapter_dac_type": "$($gpu.adapterdactype)",
	"gpu_adapter_ram": "$($gpu.adapterram)",
	"gpu_caption": "$($gpu.caption)",
	"gpu_color_table_entries": ["$(($gpu.colortableentries -join '","'))"],
	"gpu_current_refresh_rate": $($gpu.currentrefreshrate),
	"gpu_description": "$($gpu.description)",
	"gpu_driver_date": "$($gpu.driverdate)",
	"gpu_driver_version": "$($gpu.driverversion)",
	"gpu_inf_file_name": "$($gpu.inffilename)",
	"gpu_inf_section": "$($gpu.infsection)",
	"gpu_install_date": "$($gpu.installdate)",
	"gpu_last_error_code": "$($gpu.lasterrorcode)",
	"gpu_status": "$($gpu.status)",
	"gpu_status_info": "$($gpu.statusinfo)",
	"disks": [$($disks_formatted = New-Object System.Collections.Generic.List[System.Object];Foreach($disk in $disks){
	$disks_formatted.Add("
	{
		`"disk_caption`": `"$($disk.caption)`",
		`"disk_compression_method`": `"$($disk.compressionmethod)`",
		`"disk_description`": `"$($disk.description)`",
		`"disk_default_block_size`": `"$($disk.defaultblocksize)`",
		`"disk_firmware_revision`": `"$($disk.firmwarerevision)`",
		`"disk_index`": $($disk.index),
		`"disk_interface_type`": `"$($disk.interfacetype)`",
		`"disk_manufacturer`": `"$($disk.manufacturer)`",
		`"disk_model`": `"$($disk.model)`",
		`"disk_serial`": `"$($disk.serialnumber)`",
		`"disk_size`": $($disk.size),
		`"disk_status`": `"$($disk.status)`",
		`"disk_status_info`": `"$($disk.statusinfo)`",
		`"disk_total_cylinders`": $($disk.totalcylinders),
		`"disk_total_heads`": $($disk.totalheads),
		`"disk_total_sectors`": $($disk.totalsectors),
		`"disk_total_tracks`": $($disk.totaltracks)
	}
	")
	}($disks_formatted -join ','))]
}
"@