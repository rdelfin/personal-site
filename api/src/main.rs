use crate::protos::api::{
    personal_site_api_server::{PersonalSiteApi, PersonalSiteApiServer},
    {EchoRequest, EchoResponse},
};
use anyhow::Result;
use log::{error, info};
use tonic::{transport::Server, Request, Response, Status};

mod protos;

#[derive(Default)]
pub struct ApiImpl {}

#[tonic::async_trait]
impl PersonalSiteApi for ApiImpl {
    async fn echo(&self, request: Request<EchoRequest>) -> Result<Response<EchoResponse>, Status> {
        info!(
            "Got a request from {:?}: {:?}",
            request.remote_addr(),
            request.get_ref()
        );
        let reply = EchoResponse {
            echo: format!(
                "{}, {}, {}",
                request.get_ref().msg,
                request.get_ref().msg,
                request.get_ref().msg
            ),
        };
        Ok(Response::new(reply))
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    simple_logger::init_with_level(log::Level::Info).unwrap();

    if let Err(e) = do_main().await {
        error!("Error caught in main! {}", e);
        return Err(e);
    }
    Ok(())
}

async fn do_main() -> Result<()> {
    let addr = "[::1]:50051".parse().unwrap();
    let greeter = ApiImpl::default();

    info!("Echo server listening on {}", addr);

    Server::builder()
        .add_service(PersonalSiteApiServer::new(greeter))
        .serve(addr)
        .await?;

    Ok(())
}
