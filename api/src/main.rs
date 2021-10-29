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
use std::convert::TryInto;
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
        _request: Request<SendEmailRequest>,
    ) -> Result<Response<SendEmailResponse>, Status> {
        Err(Status::unimplemented("Send email hasn't been implemented"))
    }

    async fn list_projects(
        &self,
        _: Request<ListProjectsRequest>,
    ) -> Result<Response<ListProjectsResponse>, Status> {
        let projects = self.db.lock().await.list_projects().await?;
        Ok(Response::new(ListProjectsResponse { projects }))
    }

    async fn get_project(
        &self,
        request: Request<GetProjectRequest>,
    ) -> Result<Response<GetProjectResponse>, Status> {
        let project = self
            .db
            .lock()
            .await
            .get_project(request.into_inner().id.try_into().unwrap())
            .await?;
        Ok(Response::new(GetProjectResponse {
            project: Some(project),
        }))
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
