use crate::{
    db::DBManager,
    protos::api::{
        personal_site_api_server::{PersonalSiteApi, PersonalSiteApiServer},
        GetProjectRequest, GetProjectResponse, ListProjectsRequest, ListProjectsResponse,
        SendEmailRequest, SendEmailResponse,
    },
};
use anyhow::Result;
use log::{error, info};
use tokio::sync::Mutex;
use tonic::{transport::Server, Request, Response, Status};

mod db;
mod protos;

pub struct ApiImpl {
    db: Mutex<DBManager>,
}

impl ApiImpl {
    async fn new() -> anyhow::Result<Self> {
        Ok(ApiImpl {
            db: Mutex::new(DBManager::new().await?),
        })
    }
}

#[tonic::async_trait]
impl PersonalSiteApi for ApiImpl {
    async fn send_email(
        &self,
        request: Request<SendEmailRequest>,
    ) -> Result<Response<SendEmailResponse>, Status> {
        Err(Status::unimplemented("Send email hasn't been implemented"))
    }

    async fn list_projects(
        &self,
        request: Request<ListProjectsRequest>,
    ) -> Result<Response<ListProjectsResponse>, Status> {
        Err(Status::unimplemented(
            "project list hasn't been implemented",
        ))
    }

    async fn get_project(
        &self,
        request: Request<GetProjectRequest>,
    ) -> Result<Response<GetProjectResponse>, Status> {
        Err(Status::unimplemented("get project hasn't been implemented"))
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
    let greeter = ApiImpl::new().await?;

    info!("Echo server listening on {}", addr);

    Server::builder()
        .add_service(PersonalSiteApiServer::new(greeter))
        .serve(addr)
        .await?;

    Ok(())
}
