import datetime

from src.winrm.windows import WINRM_TRANSPORT, WINRM_PROTOCOL, WinRMConnection, Response
from src.util.task_formatter import TaskFormatter as tf
from src.winrm.host_group import HostGroup
from pydantic import BaseModel
from typing import NamedTuple
import logging


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
    monitors: list[Monitor]
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


class KB(NamedTuple):
    kb_caption: str
    kb_description: str
    kb_comments: str
    kb_id: str
    kb_install_date: datetime.date
    kb_name: str
    kb_status: str
    kb_installed_by: str


class NonEssential(BaseModel):
    services: list[Service]
    shares: list[Share]
    kbs: list[KB]


class WMITaskGroup:
    essential = open('essential.ps1')
    secondary = open('secondary.ps1')
    tertiary = open('tertiary.ps1')
    nonessential = open('nonessential.ps1')

    tasks = [{'name': 'Essential',
              'tasks': WinRMConnection.encode_command(essential.read())},
             {'name': "Secondary",
              'tasks': WinRMConnection.encode_command(secondary.read())},
             {'name': "Tertiary",
              'tasks': WinRMConnection.encode_command(tertiary.read())},
             {'name': 'Non-Essential',
              'tasks': WinRMConnection.encode_command(nonessential.read())}]

    essential.close()
    secondary.close()
    tertiary.close()
    nonessential.close()

    async def __execute_task(self, endpoint, user, db_handler):
        connection_string = f"{endpoint['protocol']}://{endpoint['hostname']}:{endpoint['port']}"
        connection: WinRMConnection = WinRMConnection(endpoint=connection_string,
                                                      username=user.username,
                                                      password=user.password,
                                                      server_cert_validation='ignore',
                                                      transport=endpoint['transport'])
        logging.debug(f"Connecting to Endpoint {endpoint}")

        if connection.shell_id is not None:
            logging.debug("Entering TaskGroup loop")
            for i in self.tasks:
                await connection.connect()
                for task_name, encoded in i.items():
                    logging.debug("Executing task")
                    res: tuple[str] | None = await connection.execute_ps(encoded=encoded)
                    logging.debug("Parsing Response")
                    response: Response | None = None if res is None else Response(res)
                    logging.debug("Cheking for Errors")
                    if response is None or response.status_code != 0:
                        self.result_skeleton["Hostname"] = connection.transport.endpoint
                        logging.info(self.result_skeleton | {"Status": "Failure",
                                                             "Task Name": task_name,
                                                             "Error Code": "No response" if not response
                                                             else response.std_err})
                        continue
                    self.result_skeleton["Hostname"] = connection.transport.endpoint
                    data = self.result_skeleton | {"Status": "OK",
                                                    "Task Name": task_name,
                                                    "Results": await tf.csv_to_dict(response.std_out)}
                    logging.info(data)
                    await db_handler.insert(collection='wmi_task',
                                            data=data)
                    self.success.append(connection.hostname)
                await connection.dispose()
