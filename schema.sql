--
-- PostgreSQL database dump
--

\restrict 4oWsQNIpzOnpOXzwOY9iW95LalSMjwyYJzMD5pJIWk7QIxhUPRXv5Al93AdYm70

-- Dumped from database version 16.11 (Debian 16.11-1.pgdg12+1)
-- Dumped by pg_dump version 16.11 (Homebrew)

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
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cases; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cases (
    id text NOT NULL,
    ders text,
    konu text,
    title text,
    case_text text NOT NULL,
    tags jsonb,
    source text,
    version integer DEFAULT 1,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.cases OWNER TO postgres;

--
-- Name: document_chunks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.document_chunks (
    id bigint NOT NULL,
    document_id text,
    chunk_index integer NOT NULL,
    content text NOT NULL,
    embedding public.vector(384),
    meta jsonb,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.document_chunks OWNER TO postgres;

--
-- Name: document_chunks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.document_chunks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.document_chunks_id_seq OWNER TO postgres;

--
-- Name: document_chunks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.document_chunks_id_seq OWNED BY public.document_chunks.id;


--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id text NOT NULL,
    ders text,
    konu text,
    title text,
    file_path text NOT NULL,
    mime_type text,
    file_hash text,
    version integer DEFAULT 1,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: hukuki_kaynaklar; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW public.hukuki_kaynaklar AS
 SELECT d.title,
    c.content,
    c.embedding
   FROM (public.document_chunks c
     JOIN public.documents d ON ((d.id = c.document_id)));


ALTER VIEW public.hukuki_kaynaklar OWNER TO postgres;

--
-- Name: questions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.questions (
    id text NOT NULL,
    ders text,
    konu text,
    difficulty integer,
    question_text text NOT NULL,
    options jsonb NOT NULL,
    correct_index integer NOT NULL,
    explanation text,
    tags jsonb,
    source text,
    version integer DEFAULT 1,
    created_at timestamp with time zone DEFAULT now()
);


ALTER TABLE public.questions OWNER TO postgres;

--
-- Name: quiz_attempt_answers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quiz_attempt_answers (
    id bigint NOT NULL,
    attempt_id text NOT NULL,
    user_id text NOT NULL,
    "timestamp" text NOT NULL,
    question_id text NOT NULL,
    ders text,
    konu text,
    selected_option integer NOT NULL,
    correct_option integer NOT NULL,
    is_correct integer NOT NULL,
    confidence double precision,
    retrieval_score double precision
);


ALTER TABLE public.quiz_attempt_answers OWNER TO postgres;

--
-- Name: quiz_attempt_answers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.quiz_attempt_answers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.quiz_attempt_answers_id_seq OWNER TO postgres;

--
-- Name: quiz_attempt_answers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.quiz_attempt_answers_id_seq OWNED BY public.quiz_attempt_answers.id;


--
-- Name: document_chunks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_chunks ALTER COLUMN id SET DEFAULT nextval('public.document_chunks_id_seq'::regclass);


--
-- Name: quiz_attempt_answers id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempt_answers ALTER COLUMN id SET DEFAULT nextval('public.quiz_attempt_answers_id_seq'::regclass);


--
-- Name: cases cases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cases
    ADD CONSTRAINT cases_pkey PRIMARY KEY (id);


--
-- Name: document_chunks document_chunks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_chunks
    ADD CONSTRAINT document_chunks_pkey PRIMARY KEY (id);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: questions questions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.questions
    ADD CONSTRAINT questions_pkey PRIMARY KEY (id);


--
-- Name: quiz_attempt_answers quiz_attempt_answers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz_attempt_answers
    ADD CONSTRAINT quiz_attempt_answers_pkey PRIMARY KEY (id);


--
-- Name: idx_attempt_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_attempt_id ON public.quiz_attempt_answers USING btree (attempt_id);


--
-- Name: idx_doc_chunks_doc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_doc_chunks_doc ON public.document_chunks USING btree (document_id);


--
-- Name: idx_user_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_user_id ON public.quiz_attempt_answers USING btree (user_id);


--
-- Name: document_chunks document_chunks_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.document_chunks
    ADD CONSTRAINT document_chunks_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict 4oWsQNIpzOnpOXzwOY9iW95LalSMjwyYJzMD5pJIWk7QIxhUPRXv5Al93AdYm70

