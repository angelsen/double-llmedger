import { drizzle } from 'drizzle-orm/better-sqlite3';
import Database from 'better-sqlite3';
import { env } from '$env/dynamic/private';

// Get database URL from environment variables
if (!env.DATABASE_URL) {
  throw new Error('DATABASE_URL is not set');
}

// Create a simple database connection
const client = new Database(env.DATABASE_URL);

// Only enable foreign keys for data integrity
client.pragma('foreign_keys = ON');

// Export database instance
export const db = drizzle(client);