pub mod ssh {
    use async_ssh2_tokio::client::{Client, AuthMethod, ServerCheckMethod};
    use base64::Engine;
    use utf16string::{LittleEndian, WString};
    pub struct Host{
        pub endpoint: String,
        pub port: Option<u16>,
        pub auth_method: AuthMethod,
        pub server_check_method: ServerCheckMethod,
        pub username: String
    }
    async fn connect(host: &Host) -> Option<Client>{
        let client: Option<Client> = match Client::connect(
            (host.endpoint.as_str(), host.port.unwrap_or(22)),
            host.username.as_str(),
            host.auth_method.to_owned(),
            host.server_check_method.to_owned()
        ).await{
            Err(async_ssh2_tokio::Error::KeyAuthFailed) => {
                eprintln!("Keyed authentication failed for host {}", host.endpoint);
                None
            },
            Err(async_ssh2_tokio::Error::KeyInvalid(err)) => {
                eprintln!("Keyed authentication failed for host {} with message: {}", host.endpoint, err);
                None
            },
            Err(async_ssh2_tokio::Error::PasswordWrong) => {
                eprintln!("Wrong password for host {}", host.endpoint);
                None
            },
            Err(async_ssh2_tokio::Error::AddressInvalid(_)) => {
                eprintln!("Invalid address: {}", host.endpoint);
                None
            },
            Err(async_ssh2_tokio::Error::CommandDidntExit) => {
                eprintln!("Host {}\t\tCommand didn't exit", host.endpoint);
                None
            },
            Err(async_ssh2_tokio::Error::ServerCheckFailed) => {
                eprintln!("Server check failed for host {}", host.endpoint);
                None
            },
            Err(async_ssh2_tokio::Error::SshError(err)) => {
                eprintln!("SSH Error {}", err);
                None
            },
            Err(err) => panic!("Unknown error {}", err),
            Ok(client) => Some(client)
        };
        
        client
    }
    fn encode_command(cmd: &str) -> String{
       return base64::engine::general_purpose::STANDARD.encode(WString::<LittleEndian>::from(cmd).into_bytes().as_slice());
    }
    pub async fn execute_cmd(host: &Host, command: Option<&str>, commands: Option<Vec<String>>) -> Option<(Vec<String>, Vec<String>, Vec<u32>)>{
        let client: Option<Client> = match connect(host).await{
            Some(clt) => Some(clt),
            None => {
                eprintln!("Connection failed for host {}", host.endpoint);
                None
            }
        };
        if let Some(clt) = client{
            if let Some(cmd) = command{
                let raw_result = clt.execute(cmd).await.unwrap();
                Some((vec![raw_result.stdout], vec![raw_result.stderr], vec![raw_result.exit_status]))
            } else if let Some(cmds) = commands{
                let (mut stdout, mut stderr, mut status_code): (Vec<String>, Vec<String>, Vec<u32>) = (Vec::new(), Vec::new(), Vec::new());
                for i in cmds{
                    let raw_result = clt.execute(i.as_str()).await.unwrap();
                    stdout.push(raw_result.stdout);
                    stderr.push(raw_result.stderr);
                    status_code.push(raw_result.exit_status);
                }
                Some((stdout, stderr, status_code))
            } else {
                None
            }
        }else {
            None
        }
    }
    pub async fn execute_ps(host: &Host, command: Option<&str>, commands: Option<Vec<&str>>) -> Option<(Vec<String>, Vec<String>, Vec<u32>)>{
        if let Some(cmd) = command {
            println!("{}", encode_command(cmd));
            return Some(execute_cmd(host, Some(format!("powershell -encodedcommand {command}", command=encode_command(cmd)).as_str()), None).await.unwrap());
        }else if let Some(cmds) = commands {
            let mut cmds_encoded = Vec::new();
            for i in cmds{
                cmds_encoded.push(format!("powershell -encodedcomamnd {command}", command=encode_command(i)));
            }
            return Some(execute_cmd(host, None, Some(cmds_encoded)).await.unwrap())
        }else {
            None
        }
    }
}
