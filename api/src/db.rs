use sqlx::{sqlite::SqliteConnection, Connection};

pub struct DBManager {
    conn: SqliteConnection,
}

impl DBManager {
    pub async fn new() -> Result<Self, sqlx::Error> {
        Ok(DBManager {
            conn: SqliteConnection::connect("sqlite::memory:").await?,
        })
    }

    pub async fn sample_query(&mut self) -> Result<(), sqlx::Error> {
        let row: (i64,) = sqlx::query_as("SELECT $1")
            .bind(150_i64)
            .fetch_one(&mut self.conn)
            .await?;

        println!("Got query: {:?}", row);

        Ok(())
    }
}
