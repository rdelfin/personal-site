use crate::protos::api::{Project, ProjectSummary};
use sqlx::{sqlite::SqliteConnection, Connection};
use std::convert::TryInto;
use thiserror::Error;

#[derive(Error, Debug)]
pub enum Error {
    #[error("SQLX Error")]
    SqlxError(#[from] sqlx::Error),
    #[error("Project with ID {0} doesn't exist")]
    ProjectNotFound(i64),
}

pub type Result<T, E = Error> = std::result::Result<T, E>;

pub struct DBManager {
    conn: SqliteConnection,
}

impl DBManager {
    pub async fn new() -> Result<Self, sqlx::Error> {
        Ok(DBManager {
            conn: SqliteConnection::connect("sqlite::memory:").await?,
        })
    }

    pub async fn list_projects(&mut self) -> Result<Vec<ProjectSummary>> {
        let rows: Vec<(i64, String, String, String)> =
            sqlx::query_as("SELECT id, title, image_url, short_desc FROM Project")
                .fetch_all(&mut self.conn)
                .await?;

        Ok(rows
            .into_iter()
            .map(|(id, title, image_url, short_desc)| ProjectSummary {
                id: id.try_into().unwrap(),
                title,
                image_url,
                short_desc,
            })
            .collect())
    }

    pub async fn get_project(&mut self, id: i64) -> Result<Project> {
        let row: Option<(i64, String, String, String)> =
            sqlx::query_as("SELECT id, title, image_url, content FROM Project WHERE id=$1")
                .bind(id)
                .fetch_optional(&mut self.conn)
                .await?;
        let row = row.ok_or_else(|| Error::ProjectNotFound(id))?;

        Ok(Project {
            id: row.0.try_into().unwrap(),
            title: row.1,
            image_url: row.2,
            content_md: row.3,
        })
    }
}
