--
-- PostgreSQL database dump
--

-- Dumped from database version 12.10 (Ubuntu 12.10-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 14.5 (Ubuntu 14.5-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: fintrackschema; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA fintrackschema;


ALTER SCHEMA fintrackschema OWNER TO postgres;

--
-- Name: SCHEMA fintrackschema; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA fintrackschema IS 'Schema for the FinTrack Project';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: categories; Type: TABLE; Schema: fintrackschema; Owner: postgres
--

CREATE TABLE fintrackschema.categories (
    category_name character varying(50) NOT NULL,
    category_discription character varying(500)
);


ALTER TABLE fintrackschema.categories OWNER TO postgres;

--
-- Name: TABLE categories; Type: COMMENT; Schema: fintrackschema; Owner: postgres
--

COMMENT ON TABLE fintrackschema.categories IS 'Categories of transactions';


--
-- Name: COLUMN categories.category_name; Type: COMMENT; Schema: fintrackschema; Owner: postgres
--

COMMENT ON COLUMN fintrackschema.categories.category_name IS 'name of the specifi category';


--
-- Name: COLUMN categories.category_discription; Type: COMMENT; Schema: fintrackschema; Owner: postgres
--

COMMENT ON COLUMN fintrackschema.categories.category_discription IS 'more detailed discription of the categoy';


--
-- Name: transactions; Type: TABLE; Schema: fintrackschema; Owner: postgres
--

CREATE TABLE fintrackschema.transactions (
    transaction_id integer NOT NULL,
    transaction_name character varying(50) NOT NULL,
    transaction_description character varying(500),
    transaction_category character varying(50) NOT NULL,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    betrag real NOT NULL
);


ALTER TABLE fintrackschema.transactions OWNER TO postgres;

--
-- Name: TABLE transactions; Type: COMMENT; Schema: fintrackschema; Owner: postgres
--

COMMENT ON TABLE fintrackschema.transactions IS 'the different transactions of a user';


--
-- Name: COLUMN transactions.transaction_description; Type: COMMENT; Schema: fintrackschema; Owner: postgres
--

COMMENT ON COLUMN fintrackschema.transactions.transaction_description IS 'optional description of transaction';


--
-- Name: COLUMN transactions.transaction_category; Type: COMMENT; Schema: fintrackschema; Owner: postgres
--

COMMENT ON COLUMN fintrackschema.transactions.transaction_category IS 'what kind of category the transaction is primarily';


--
-- Name: COLUMN transactions."timestamp"; Type: COMMENT; Schema: fintrackschema; Owner: postgres
--

COMMENT ON COLUMN fintrackschema.transactions."timestamp" IS 'timestamp when the transaction was added to the dB';


--
-- Name: COLUMN transactions.betrag; Type: COMMENT; Schema: fintrackschema; Owner: postgres
--

COMMENT ON COLUMN fintrackschema.transactions.betrag IS 'Hoehe der Ausgabe durch die transaktion';


--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE; Schema: fintrackschema; Owner: postgres
--

CREATE SEQUENCE fintrackschema.transactions_transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE fintrackschema.transactions_transaction_id_seq OWNER TO postgres;

--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: fintrackschema; Owner: postgres
--

ALTER SEQUENCE fintrackschema.transactions_transaction_id_seq OWNED BY fintrackschema.transactions.transaction_id;


--
-- Name: transactions transaction_id; Type: DEFAULT; Schema: fintrackschema; Owner: postgres
--

ALTER TABLE ONLY fintrackschema.transactions ALTER COLUMN transaction_id SET DEFAULT nextval('fintrackschema.transactions_transaction_id_seq'::regclass);


--
-- Data for Name: categories; Type: TABLE DATA; Schema: fintrackschema; Owner: postgres
--

COPY fintrackschema.categories (category_name, category_discription) FROM stdin;
Lebensmittel	Brot, Kaese, Gemuese und Co
Entertainment	Buecher Filme Kino und Co
Transport	Sprit Bus und Co
Miete	
\.


--
-- Data for Name: transactions; Type: TABLE DATA; Schema: fintrackschema; Owner: postgres
--

COPY fintrackschema.transactions (transaction_id, transaction_name, transaction_description, transaction_category, "timestamp", betrag) FROM stdin;
1	Einkauf	Supermark:\nSchnitzel, Kartoffel, Champinons 	Lebensmittel	2022-10-14 17:21:17.561141	25.56
2	Kino	date im kino	Entertainment	2022-10-14 17:22:05.678987	40.99
3	Miete	\N	Miete	2022-10-14 17:23:20.599515	400
5	Reise nach Jerusalem	Flugzeug tickets	Transport	2022-10-14 17:24:28.580667	956
\.


--
-- Name: transactions_transaction_id_seq; Type: SEQUENCE SET; Schema: fintrackschema; Owner: postgres
--

SELECT pg_catalog.setval('fintrackschema.transactions_transaction_id_seq', 5, true);


--
-- Name: categories categories_pk; Type: CONSTRAINT; Schema: fintrackschema; Owner: postgres
--

ALTER TABLE ONLY fintrackschema.categories
    ADD CONSTRAINT categories_pk PRIMARY KEY (category_name);


--
-- Name: transactions transactions_pk; Type: CONSTRAINT; Schema: fintrackschema; Owner: postgres
--

ALTER TABLE ONLY fintrackschema.transactions
    ADD CONSTRAINT transactions_pk PRIMARY KEY (transaction_id);


--
-- Name: transactions transactions_Categories_null_fk; Type: FK CONSTRAINT; Schema: fintrackschema; Owner: postgres
--

ALTER TABLE ONLY fintrackschema.transactions
    ADD CONSTRAINT "transactions_Categories_null_fk" FOREIGN KEY (transaction_category) REFERENCES fintrackschema.categories(category_name);


--
-- PostgreSQL database dump complete
--

