DO $$ 
BEGIN
    -- Verifica se a tabela "atendimentos" existe
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'atendimentos') THEN
        CREATE TABLE atendimentos (
            order_number SERIAL PRIMARY KEY,
            terminal_id INTEGER,
            terminal_serial_number VARCHAR,
            terminal_model VARCHAR,
            arrival_date TIMESTAMP,
            deadline_date TIMESTAMP,
            cancellation_reason TEXT,
            last_modified_date TIMESTAMP,
            country_state VARCHAR,
            technician_email VARCHAR,
            zip_code VARCHAR,
            neighborhood VARCHAR,
            customer_phone VARCHAR,
            complement VARCHAR,
            city VARCHAR,
            customer_id VARCHAR,
            terminal_type VARCHAR,
            street_name VARCHAR,
            provider VARCHAR,
            country VARCHAR,
            image_path VARCHAR,
            exportado_para_dw BOOLEAN DEFAULT FALSE
        );
    END IF;

    -- Verifica se a tabela "lotes_processados" existe
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'lotes_processados') THEN
        CREATE TABLE lotes_processados (
            arquivo_nome VARCHAR PRIMARY KEY,
            data_processamento TIMESTAMP NOT NULL
        );
    END IF;
END $$;