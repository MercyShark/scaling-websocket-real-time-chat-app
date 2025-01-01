import psycopg2
conn = psycopg2.connect(
    dbname="slack_chatapp_db",
    user="postgres", password="root"
)

cur = conn.cursor()


try:


    cur.execute('''
-- Create 'users' table
CREATE TABLE IF NOT EXISTS users  (
    id SERIAL PRIMARY KEY ,
    name VARCHAR(50)  NOT NULL,
    email VARCHAR(50)  UNIQUE NOT NULL,
    photo TEXT,
    password TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create 'channels' table
CREATE TABLE IF NOT EXISTS channels (
    id SERIAL PRIMARY KEY,
    channel_type VARCHAR(10) NOT NULL CHECK (channel_type IN ('dm', 'group')),
    name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id) ON DELETE CASCADE,
    updated_by INTEGER REFERENCES users(id) ON DELETE CASCADE
);

-- Create 'membership' table
CREATE TABLE IF NOT EXISTS membership (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    channel_id INTEGER REFERENCES channels(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_read_at TIMESTAMP,
    muted BOOLEAN DEFAULT FALSE,
    favorite BOOLEAN DEFAULT FALSE
);

-- Create 'messages' table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    channel_id INTEGER REFERENCES channels(id) ON DELETE CASCADE,
    message TEXT,
    media_url TEXT,  -- URL or path to the media file
    media_type VARCHAR(50),  -- Type of media, e.g., 'image', 'video', 'audio', 'document'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraint: If message is NULL, media_url and media_type must be present
    CONSTRAINT chk_message_media CHECK (
        (message IS NOT NULL AND media_url IS NULL AND media_type IS NULL) OR
        (message IS NULL AND media_url IS NOT NULL AND media_type IS NOT NULL)
    )
);

''')
    
    conn.commit()

    print("Tables created")

except Exception as e:
    print(e)
    print("hell")

finally:
    cur.close()
    conn.close()
    
