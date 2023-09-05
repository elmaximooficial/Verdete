pub mod wmi{
    use serde;
    use serde::{Serialize, Deserialize};
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct baseboard {
        config_options: Vec<String>,
        depth: String,
        description: String,
        height: String,
        hosting_board: String,
        hot_swappable: String,
        install_date: String,
        manufacturer: String,
        model: String,
        name: String,
        other_identifying_info: String,
        part_number: String,
        powered_on: bool,
        product: String,
        removable: bool,
        replaceable: bool,
        requirements_description: String,
        requires_daughter_board: bool,
        serial_number: String,
        sku: String,
        slot_layout: String,
        special_requirements: String,
        status: String,
        tag: String,
        version: String,
        weight: String,
        width: String,
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct bios {
        bios_characteristics: Vec<u32>,
        build_number: String,
        code_set: Vec<String>,
        current_language: String,
        description: String,
        identification_code: String,
        installable_languages: Vec<u32>,
        install_date: String,
        list_of_languages: Vec<String>,
        manufacturer: String,
        name: String,
        other_target_os: String,
        release_date: String,
        serial_number: String,
        smbios_bios_version: String,
        smbios_major_version: String,
        smbios_minor_version: String,
        smbios_present: bool,
        software_element_id: String,
        software_element_state: u16,
        status: String,
        target_operating_system: u16,
        version: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct boot_config {
        boot_directory: String,
        configuration_path: String,
        description: String,
        last_drive: u16,
        name: String,
        scratch_directory: String,
        setting_id: String,
        temp_directory: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct computer_system {
        admin_password_status: u16,
        automatic_reset_boot_option: bool,
        automatic_reset_capability: bool,
        boot_option_on_limit: String,
        boot_option_on_watch_dog: String,
        boot_rom_supported: bool,
        bootup_state: String,
        caption: String,
        chassis_bootup_state: u16,
        creation_class_name: String,
        current_timezone: i16,
        daylight_in_effect: bool,
        description: String,
        domain: String,
        domain_role: u16,
        enable_daylight_savings_time: bool,
        front_panel_reset_status: u16,
        infrared_support: bool,
        initial_load_info: String,
        install_date: String,
        keyboard_password_status: u16,
        last_load_info: String,
        manufacturer: String,
        model: String,
        name: String,
        name_format: String,
        number_of_processors: u16,
        oem_string_array: Vec<String>,
        part_of_domain: bool,
        pause_after_reset: i8,
        power_management_capabilities: Vec<String>,
        power_management_supported: bool,
        power_on_password_status: u8,
        power_state: u8,
        power_supply_state: u8,
        primary_owner_contact: String,
        primary_owner_name: String,
        reset_capability: u8,
        reset_count: i8,
        reset_limit: i8,
        roles: Vec<String>,
        status: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct cpu {
        address_widht: u8,
        architecture: u8,
        availability: u8,
        caption: String,
        config_manager_error_code: u16,
        config_manager_user_config: u16,
        cpu_status: u8,
        creation_class_name: String,
        current_clock_speed: u16,
        current_voltage: u8,
        data_width: u8,
        description: String,
        device_id: String,
        error_cleared: String,
        error_description: String,
        ext_clock: u8,
        family: u8,
        install_date: String,
        l2_cache_size: u16,
        l2_cache_speed: u16,
        level: u8,
        load_percentage: u8,
        manufacturer: String,
        max_clock_speed: u16,
        name: String,
        other_family_description: String,
        pnp_device_id: String,
        power_management_capabilities: Vec<String>,
        power_management_supported: bool,
        processor_id: String,
        processor_type: u8,
        revision: String,
        role: String,
        socket_designation: String,
        status: String,
        status_info: u8,
        stepping: String,
        system_creation_class_name: String,
        system_name: String,
        unique_id: String,
        upgrade_method: u8,
        version: String,
        voltage_caps: Vec<String>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct csproduct {
        description: String,
        identifying_number: String,
        name: String,
        sku_number: String,
        uuid: String,
        vendor: String,
        version: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct desktop {
        border_width: u16,
        cool_switch: String,
        cursor_blink_rate: u16,
        description: String,
        drag_full_windows: bool,
        grid_granularity: u16,
        icon_spacing: u16,
        icon_title_face_name: String,
        icon_title_size: u16,
        icon_title_wrap: bool,
        name: String,
        pattern: String,
        screen_saver_active: bool,
        screen_saver_executable: String,
        screen_saver_secure: String,
        screen_saver_timeout: String,
        setting_id: String,
        wallpaper: String,
        wallpaper_stretched: bool,
        wallpaper_tiled: bool
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Desktop")]
    pub struct desktops {
        desktop_vec: Vec<desktop>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct desktop_monitor {
        availability: u8,
        bandwidth: u16,
        config_manager_error_code: u8,
        config_manager_user_config: bool,
        description: String,
        device_id: String,
        display_type: String,
        error_cleared: String,
        error_description: String,
        install_date: String,
        is_locked: bool,
        last_error_code: String,
        monitor_manufacturer: String,
        monitor_type: String,
        name: String,
        pixels_per_x_logical_inch: u16,
        pixels_per_y_logical_inch: u16,
        pnp_device_id: String,
        power_management_capabilities: Vec<String>,
        power_management_supported: bool,
        screen_height: u16,
        screen_width: u16,
        status: String,
        status_info: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "DesktopMonitor")]
    pub struct desktop_monitors {
        desktop_monitor_vec: Vec<desktop_monitor>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct disk_drive {
        availability: u16,
        bytes_per_sector: u16,
        capabilities: Vec<u8>,
        capability_descriptions: Vec<String>,
        compression_method: String,
        config_manager_error_code: u16,
        config_manager_user_config: bool,
        default_block_size: u16,
        description: String,
        device_id: String,
        error_cleared: String,
        error_description: String,
        error_methodology: String,
        index: u8,
        install_date: String,
        interface_type: String,
        manufacturer: String,
        max_block_size: u16,
        max_media_size: u16,
        media_loaded: bool,
        media_type: String,
        min_block_size: u16,
        model: String,
        name: String,
        needs_cleaning: bool,
        number_of_media_supported: u16,
        partitions: u8,
        pnp_device_id: String,
        power_management_capabilities: Vec<String>,
        power_management_supported: bool,
        scsi_bus: u8,
        scsi_logical_unit: u8,
        scsi_port: u8,
        scsi_target_id: u8,
        sectors_per_track: u16,
        signature: String,
        size: u64,
        status: String,
        status_info: String,
        total_cylinders: u32,
        total_heads: u16,
        total_sectors: u64,
        total_tracks: u32,
        tracks_per_cylinder: u16
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "DiskDrive")]
    pub struct disk_drives {
        disk_drive_vec: Vec<disk_drive>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct enviornment {
        description: String,
        install_date: String,
        name: String,
        status: String,
        system_variable: bool,
        user_name: String,
        variable_value: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Environment")]
    pub struct enviornments {
        enviornment_vec: Vec<enviornment>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct load_order {
        driver_enabled: bool,
        group_order: u16,
        name: String,
        status: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(renam = "LoadOrder")]
    pub struct load_orders {
        load_order_vec: Vec<laod_order>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct logical_disk {
        access: u8,
        availability: u8,
        block_size: u16,
        caption: String,
        compressed: bool,
        config_manager_error_code: String,
        config_manager_user_config: bool,
        description: String,
        device_id: String,
        device_type: u8,
        error_cleared: String,
        error_description: String,
        error_methodology: String,
        file_system: String,
        free_sapce: u64,
        install_date: String,
        last_error_code: String,
        maximum_component_length: u16,
        media_type: u8,
        name: String,
        number_of_blocks: u32,
        pnp_device_id: String,
        power_management_capabilities: Vec<String>,
        power_management_supported: bool,
        provider_name: String,
        purpose: String,
        quotas_disabled: bool,
        quotas_incomplete: bool,
        quotas_rebuilding: bool,
        size: u64,
        status: String,
        status_info: String,
        supports_disk_quotas: bool,
        supports_file_based_compression: bool,
        volume_name: String,
        volume_serial_number: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "LogicalDisk")]
    pub struct logical_disks {
        logical_disk_vec: Vec<logical_disk>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct logon {
        authentication_package: String,
        caption: String,
        description: String,
        install_date: String,
        logon_id: u32,
        logon_type: u8,
        name: String,
        start_time: String,
        status: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Logon")]
    pub struct logons {
        logon_vec: Vec<logon>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct memory_chip {
        bank_label: String,
        capacity: u64,
        data_width: u8,
        description: String,
        device_locator: String,
        form_factor: u8,
        hot_swappable: bool,
        install_date: String,
        interlave_data_length: u8,
        interleave_position: u8,
        manufacturer: String,
        memory_type: u8,
        model: String,
        name: String,
        other_identifying_info: String,
        part_number: String,
        position_in_row: u8,
        powered_on: bool,
        removable: bool,
        replaceable: bool,
        serial_number: String,
        sku: String,
        speed: u16,
        status: String,
        tag: String,
        total_width: u8,
        type_detail: u8,
        version: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "MemoryChip")]
    pub struct memory_chips {
        memory_chip_vec: Vec<memory_chip>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct mem_physical {
        depth: String,
        description: String,
        height: String,
        hot_swappable: bool,
        install_date: String,
        location: u8,
        manufacturer: String,
        max_capacity: u64,
        memory_device: u8,
        memory_error_correction: u8,
        model: String,
        name: String,
        other_identifying_info: String,
        part_number: String,
        powered_on: bool,
        removable: bool,
        replaceable: bool,
        serial_number: String,
        sku: String,
        status: String,
        tag: String,
        mem_use: u8,
        weight: String,
        width: String,
        version: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "PhysicalMem")]
    pub struct physical_mems {
        mem_physical_vec: Vec<mem_physical>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct netclient {
        description: String,
        install_date: String,
        manufacturer: String,
        name: String,
        status: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct nic {
        adapter_type: String,
        auto_sense: bool,
        availability: u8,
        config_manager_error_code: u8,
        config_manager_user_config: bool,
        description: String,
        device_id: u8,
        error_cleared: String,
        error_description: String,
        index: u8,
        install_date: String,
        installed: bool,
        last_error_code: String,
        mac_address: String,
        manufacturer: String,
        max_number_controlled: u8,
        max_speed: u64,
        name: String,
        net_connection_id: String,
        net_connection_status: String,
        network_addresses: Vec<String>,
        permanent_addresses: Vec<String>,
        pnp_device_id: String,
        power_management_capabilities: String,
        power_management_supported: bool,
        product_name: String,
        service_name: String,
        speed: u64,
        status: String,
        status_info: String,
        time_of_last_reset: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "NIC")]
    pub struct nics {
        nic_vec: Vec<nic>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct nic_config {
        arp_always_source_route: String,
        arp_use_ether_snap: bool,
        dead_gw_detect_enabled: bool,
        default_ip_gateway: String,
        default_tos: String,
        default_ttl: u8,
        description: String,
        dhcp_enabled: bool,
        dhcp_lease_expires: String,
        dhcp_lease_obtained: String,
        dhcp_server: String,
        dns_domain: String,
        dns_domain_suffix_search_order: Vec<String>,
        dns_enabled_for_wins_resolution: bool,
        dns_host_name: String,
        dns_server_search_order: Vec<String>,
        domain_dns_registration_enabled: bool,
        forward_buffer_memory: u64,
        full_dns_registration_enabled: bool,
        gateway_cost_metric: u64,
        igmp_level: u64,
        index: u8,
        ip_address: String,
        ip_connection_metric: String,
        ip_enabled: bool,
        ip_filter_security_enabled: bool,
        ip_port_security_enabled: bool,
        ip_sec_permit_ip_protocols: Vec<String>,
        ip_sec_permit_tcp_ports: Vec<String>,
        ip_sec_permit_udp_ports: Vec<String>,
        ip_subnet: String,
        ip_use_zero_broadcast: bool,
        ip_x_address: String,
        ip_x_enabled: bool,
        ip_x_frame_type: String,
        ip_x_media_type: String,
        ip_x_network_number: String,
        ip_x_virtual_net_number: String,
        keep_alive_interval: String,
        keep_alive_time: String,
        mac_address: String,
        mtu: u16,
        num_forward_packets: u64,
        pmtubh_detect_enabled: bool,
        pmtu_discovery_enabled: bool,
        service_name: String,
        setting_id: String,
        tcpip_netbios_options: Vec<String>,
        tpc_max_connections_retransmissions: u64,
        tcp_num_connections: u64,
        tpc_use_rfc_1122_urgent_pointer: bool,
        tcp_window_size: u32,
        wins_enable_lm_hosts_lookup: bool,
        wins_host_lookup_file: String,
        wins_primary_server: String,
        wins_scope_id: String,
        wins_secondary_server: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "NICConfig")]
    pub struct nic_configs {
        nic_config_vec: Vec<nic_config>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct port{
        alias: bool,
        description: String,
        ending_address: u64,
        name: String,
        starting_address: u64,
        status: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Port")]
    pub struct ports {
        port_vec: Vec<port>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct printer {
        attributes: u16,
        availability: u8,
        available_job_sheets: u8,
        average_pages_per_minute: u8,
        capabilites: Vec<u8>,
        capability_descriptions: Vec<String>,
        caption: String,
        char_set_supported: Vec<String>,
        comment: String,
        config_manager_error_code: String,
        config_manager_user_config: bool,
        current_capabilites: Vec<u8>,
        current_char_set: String,
        current_language: String,
        current_mime_type: String,
        current_natural_language: String,
        current_paper_type: String,
        default: bool,
        default_capabilities: Vec<u8>,
        default_copies: u8,
        default_language: String,
        default_mime_type: String,
        default_number_up: String,
        default_paper_type: String,
        default_priority: u8,
        description: String,
        detected_error_state: u8,
        device_id: String,
        direct: bool,
        do_complete_first: bool,
        driver_name: String,
        enable_bidi: bool,
        enable_dev_query_print: bool,
        error_cleared: String,
        error_description: String,
        error_information: String,
        extended_detected_error_state: u8,
        extended_printer_status: u8,
        hidden: bool,
        horizontal_resolution: u16,
        install_date: String,
        job_count_since_last_reset: u8,
        keep_printed_jobs: bool,
        languages_supported: Vec<String>,
        last_error_code: String,
        local: bool,
        location: String,
        marking_technology: String,
        max_copies: u64,
        max_number_up: String,
        max_size_supported: u64,
        mime_types_supported: Vec<String>,
        name: String,
        paper_sizes_supported: Vec<u8>,
        pnp_device_id: String,
        port_name: String,
        power_management_capabilities: Vec<String>,
        power_management_supported: bool,
        printer_paper_names: Vec<String>,
        printer_state: u8,
        printer_status: u8,
        print_job_data_type: String,
        print_processor: String,
        separator_file: String,
        server_name: String,
        share_name: String,
        spool_enabled: bool,
        start_time: String,
        status: String,
        status_info: String,
        time_of_last_reset: String,
        until_time: String,
        vertical_resolution: u16
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Printer")]
    pub struct printers {
        printer_vec: Vec<printer>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct product {
        description: String,
        id: String,
        install_date: String,
        install_location: String,
        install_state: u8,
        name: String,
        package_cache: String,
        sku: String,
        vendor: String,
        version: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")]
    #[serde(rename = "Product")] 
    pub struct products {
        product_vec: Vec<product>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct qfe {
        caption: String,
        description: String,
        fix_comments: String,
        hot_fix_id: String,
        install_date: String,
        installed_by: String,
        installed_on: String,
        name: String,
        service_pack_in_effect: String,
        status: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "QFE")]
    pub struct qfes {
        qfe_vec: Vec<qfe>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct recoveros {
        auto_reboot: bool,
        debug_file_path: String,
        description: String,
        kernel_dump_only: bool,
        name: String,
        overwrite_existing_debug_file: bool,
        send_admin_alert: bool,
        settign_id: String,
        write_debug_info: bool,
        write_to_system_log: bool
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "RecoverOS")]
    pub struct os_recoveries {
        recoveros_vec: Vec<recoveros>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct registry {
        current_size: u16,
        description: String,
        install_date: String,
        maximum_size: u16,
        name: String,
        proposed_size: u16,
        status: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct service {
        accept_pause: bool,
        accept_stop: bool,
        caption: String,
        check_point: u8,
        creation_class_name: String,
        description: String,
        desktop_interact: String,
        display_name: String,
        error_control: String,
        exit_code: String,
        install_date: String,
        name: String,
        path_name: String,
        process_id: String,
        service_specific_exit_code: u16,
        service_type: u8,
        started: String,
        start_mode: String,
        start_name: String,
        state: String,
        status: String,
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Service")]
    pub struct services {
        service_vec: Vec<service>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct share {
        access_mask: String,
        allow_maximum: String,
        description: String,
        install_date: String,
        maximum_allowed: u16,
        name: String,
        path: String,
        status: String,
        share_type: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Share")]
    pub struct shares {
        share_vec: Vec<share>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct sound_dev {
        description: String,
        device_id: String,
        dma_buffer_size: String,
        error_cleared: String,
        error_description: String,
        install_date: String,
        last_error_code: String,
        manufacturer: String,
        mpu_401_address: String,
        name: String,
        pnp_device_id: String,
        product_name: String,
        status: String,
        status_info: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "SoundDev")]
    pub struct sound_devs {
        sound_dev_vec: Vec<sound_dev>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct startup {
        caption: String,
        command: String,
        description: String,
        location: String,
        setting_id: String,
        user: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Startup")]
    pub struct startup_servs{
        startup_vec: Vec<startup>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct sysaccount {
        description: String,
        domain: String,
        install_date: String,
        local_account: bool,
        name: String,
        sid: String,
        sid_type: u8,
        status: String
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "SysAccount")]
    pub struct sysaccounts {
        sysaccount_vec: Vec<sysaccount>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct sysdriver {
        accept_pause: bool,
        accept_stop: bool,
        description: String,
        desktop_interact: bool,
        display_name: String,
        error_control: String,
        exit_code: u8,
        install_date: String,
        name: String,
        path_name: String,
        service_specific_exit_code: u8,
        service_type: String,
        started: bool,
        start_mode: String,
        start_name: String,
        state: String,
        status: String,
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "SysDriver")]
    pub struct sysdrivers {
        sysdriver_vec: Vec<sysdriver>
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    pub struct volume {
        block_size: u16,
        capacity : u64,
        compressed: bool,
        device_id: String,
        diry_bit_set: bool,
        drive_letter: String,
        file_system: String,
        free_space: u64,
        indexing_enabled: bool,
        label: String,
        maximum_file_name_length: u16,
        name: String,
        quotas_enabled: bool,
        quotas_incomplete: bool,
        quotas_rebuilding: bool,
        serial_number: String,
        supports_disk_quotas: bool,
        supports_file_based_compression: bool
    }
    #[derive(Serialize, Deserialize, Debug, Clone)]
    #[serde(rename_all = "PascalCase")] 
    #[serde(rename = "Volume")]
    pub struct volumes {
        volume_vec: Vec<volume>
    }
}