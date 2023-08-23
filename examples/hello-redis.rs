use mini_redis::{client, Result};

#[tokio::main]
async fn main() -> Result<()> {
    let mut client = client::connect("10.250.240.9:6379").await?;

    client.set("Hello", "World".into()).await?;

    let result = client.get("Hello").await?;
    println!("Got value from server; result={:?}", result);

    Ok(())
}