use async_trait::async_trait;

pub mod mongodb_handler{
    use std::{fs, path::Path};
    use serde::Deserialize;
    use mongodb::{options::{Compressor, Credential, ClientOptions, ServerAddress}, Client, Collection};
    use async_trait::async_trait;

    #[derive(Deserialize, Debug)]
    pub struct MongoDBConfig{
        MongoDBHandler: MongoDBHandler
    }
    #[derive(Deserialize, Debug)]
    pub struct MongoDBHandler{
        username: String,
        password: String,
        host: Vec<String>,
        port: u16,
        #[serde(skip_deserializing)]
        compressors: Option<Vec<Compressor>>
    }

    pub fn fetch_from_file(filepath: &str) -> MongoDBHandler{
        let mongodb_config: MongoDBConfig = toml::from_str(
                                                &fs::read_to_string(Path::new(filepath)).unwrap().as_str()
                                                ).unwrap();
        return mongodb_config.MongoDBHandler
    }

    impl MongoDBHandler{
        pub async fn connect(&self) -> Client{
            let hosts = &self.host;
            let credential: Credential = Credential::builder()
                                                    .username(self.username.clone())
                                                    .password(self.password.clone())
                                                    .build();
            let mut server_addresses: Vec<ServerAddress> = Vec::new();
            for i in hosts{
                server_addresses.push(ServerAddress::Tcp { host: i.clone(), port: Some(self.port) });
            }
            let options: ClientOptions = ClientOptions::builder()
                                                        .hosts(server_addresses)
                                                        .compressors(self.compressors.clone())
                                                        .credential(credential)
                                                        .build();
                                                        
            let client = mongodb::Client::with_options(options).unwrap();
            return client
        }
        pub async fn get_collection<T>(&self, client: &Client, name: &str) -> Collection<T>{
            return client.database("verdete").collection::<T>(name);
        }
    }


}