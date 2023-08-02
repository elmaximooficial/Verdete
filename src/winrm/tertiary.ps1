$bios = Get-WMiObject WIn32_BIOS | Select-Object BiosCharacteristics, BIOSVersion, BuildNumber, Caption, CurrentLanguage, Description, InstallDate, Manufacturer, Name, SerialNumber, ReleaseDate
$monitors = Get-WmiObject Win32_DesktopMonitor | Select-Object Caption, Description, MonitorManufacturer, MonitorType, Name, PixelsPerLogicalXInch, PixelsPerLogicalYInch, ScreenHeight, ScreenWidth, Status, StatusInfo
$keyboard = Get-WmiObject Win32_Keyboard | Select-Object Caption, Description, Name, Status, StatusInfo
$mouse = Get-WmiObject Win32_PointingDevice | Select-Object Caption, Description, HardwareType, InfFIleName, InfSection, Manufacturer, Name, NumberOfButtons, PointingType, Status, StatusInfo
$products = Get-WmiObject Win32_Product | Select-Object Caption, Description, IdentifyingNumber, InstallDate, InstallSource, LocalPackage, Name, PackageName, ProductID, SKUNumber, Version, Vendor

@"
{
  "bios_characteristics": ["$($bios.BiosCharacteristics -join '","')"],
  "bios_version": "$($bios.version)",
  "bios_build_number": "$($bios.buildnumber)",
  "bios_caption": "$($bios.caption)",
  "bios_current_language": "$($bios.CurrentLanguage)",
  "bios_description": "$($bios.Description)",
  "bios_install_date": "$($bios.InstallDate)",
  "bios_manufacturer": "$($bios.Manufacturer)",
  "bios_name": "$($bios.Name)",
  "bios_serial": "$($bios.SerialNumber)",
  "bios_release_date": "$($bios.ReleaseDate)",
  "keyboard_caption": "$($keyboard.caption)",
  "keyboard_description": "$($keyboard.Description)",
  "keyboard_name": "$($keyboard.Name)",
  "keyboard_status": "$($keyboard.Status)",
  "keyboard_status_info": "$($keyboard.StatusInfo)",
  "mouse_caption": "$($mouse.caption)",
  "mouse_description": "$($mouse.Description)",
  "mouse_hardware_type": "$($mouse.HardwareType)",
  "mouse_inf_file_name": "$($mouse.InfFIleName)",
  "mouse_inf_section": "$($mouse.InfSection)",
  "mouse_manufacturer": "$($mouse.Manufacturer)",
  "mouse_name": "$($mouse.Name)",
  "mouse_number_of_buttons": $($mouse.NumberOfButtons),
  "mouse_pointing_type": "$($mouse.PointingType)",
  "mouse_status": "$($mouse.Status)",
  "mouse_status_info": "$($mouse.StatusInfo)",
  "monitors": [$($monitors_formatted = New-Object System.Collections.Generic.List[System.Object];foreach($monitor in $monitors){
    $monitors_formatted.Add("
    {
      `"monitor_caption`": `"$($monitor.caption)`",
      `"monitor_description`": `"$($monitor.Description)`",
      `"monitor_manufacturer`": `"$($monitor.Manufacturer)`",
      `"monitor_type`": `"$($monitor.MonitorType)`",
      `"monitor_name`": `"$($monitor.name)`",
      `"monitor_pixels_per_logical_x_inch`": `"$($monitor.PixelsPerLogicalXInch)`",
      `"monitor_pixels_per_logical_y_inch`": `"$($monitor.PixelsPerLogicalYInch)`",
      `"monitor_screen_height`": `"$($monitor.ScreenHeight)`",
      `"monitor_screen_width`": `"$($monitor.ScreenWidth)`",
      `"monitor_status`": `"$($monitor.Status)`",
      `"monitor_status_info`": `"$($monitor.StatusInfo)`"
    }
    ")
  }($monitors_formatted -join ','))],
  "products": [$($products_formatted = New-Object System.Collections.Generic.List[System.Object];foreach($product in $products){
    $products_formatted.Add("
    {
      `"product_caption`": `"$($product.caption)`",
      `"product_description`": `"$($product.Description)`",
      `"product_id`": `"$($product.IdentifyingNumber)`",
      `"product_install_date`": `"$($product.InstallDate)`",
      `"product_install_source`": `"$(if($null -ne $product.InstallSource){
        ($product.InstallSource).replace("\", "\\")
      }else{
        "null"
      })`",
      `"product_local_package`": `"$(if($null -ne $product.LocalPackage){
        ($product.LocalPackage).replace("\", "\\")
      }else{
        "null"
      })`",
      `"product_name`": `"$($product.name)`",
      `"product_package_name`": `"$($product.PackageName)`",
      `"product_package_sku`": `"$($product.SKUNumber)`",
      `"product_version`": `"$($product.version)`",
      `"product_vendor`": `"$($product.Vendor)`"
    }
    ")
  } ($products_formatted -join ',') )]
}
"@