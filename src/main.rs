pub mod windows;

use windows::transport::ssh;

#[tokio::main]
async fn main(){
    let tasks = vec![];
    
    let host = ssh::Host{
        endpoint: "192.168.8.218".to_owned(),
        port: None,
        auth_method: async_ssh2_tokio::AuthMethod::Password("cpd@pmpa".to_owned()),
        server_check_method: async_ssh2_tokio::ServerCheckMethod::NoCheck,
        username: "instalar.cpd".to_owned()
    };
    let (stdout, stderr, status_code) = ssh::execute_cmd(&host, Some("wmic os list brief"), None).await.unwrap();
    println!("{:?}\n{:?}\n{:?}", stdout, stderr, status_code);
    let (stdout, stderr, status_code) = ssh::execute_ps(&host, Some("Get-WmiObject Win32_OperatingSystem"), None).await.unwrap();
    println!("{:?}\n{:?}\n{:?}", stdout, stderr, status_code);
}