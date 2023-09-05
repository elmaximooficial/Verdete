use async_trait::async_trait;
use ldap3::Ldap;

#[async_trait]
pub trait Injector{
    async fn fetch_names(connection: &'static mut Ldap, filter: String) -> Vec<String>;
}

pub mod ldap_injector{

    use async_trait::async_trait;
    use ldap3::{Scope, SearchEntry};

    #[derive(Debug)]
    pub enum LDAPProtocol{
        LDAP,
        LDAPS
    }

    #[derive(Debug)]
    pub struct LDAPInjector<'a>{
        pub url: String,
        pub port: &'a u16,
        pub protocol: LDAPProtocol,
        pub kdc_fqdn: String,
        pub default_search_base: String
    }
    
    #[async_trait]
    pub trait Injector{
        async fn fetch(&self, search_base: String) -> Vec<String>;
    }
    
    #[async_trait]
    impl<'a> Injector for LDAPInjector<'a>{
        async fn fetch(&self, search_base: String) -> Vec<String>{
            let proto = match &self.protocol{
                LDAPProtocol::LDAP => "ldap://",
                LDAPProtocol::LDAPS => "ldaps://"
            };
            let (conn_async, mut ldap) = ldap3::LdapConnAsync::new(&format!("{}{}:{}", 
                                                                    &proto,
                                                                    &self.url,
                                                                    &self.port
                                                                    )).await.unwrap();
            ldap3::drive!(conn_async);
            ldap.sasl_gssapi_bind(&self.kdc_fqdn).await.unwrap();
            let mut computers: Vec<String> = Vec::new();
            computers = tokio::spawn(async move{
                let mut handler = ldap.streaming_search(&search_base, 
                                                                                        Scope::Subtree, 
                                                                                        "(objectClass=computer)", 
                                                                                        vec!["dnshostname"]).await.unwrap();
                while let Some(result) = handler.next().await.unwrap(){
                    computers.push(SearchEntry::construct(result).attrs["dNSHostName"][0].clone());
                }
                handler.finish().await;
                computers
            }).await.unwrap();
            return computers
        }
    }

}