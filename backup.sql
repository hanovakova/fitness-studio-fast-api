--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1.pgdg120+2)
-- Dumped by pg_dump version 17.4 (Debian 17.4-1.pgdg120+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: fitness_classes; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.fitness_classes (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text,
    start_time timestamp without time zone,
    end_time timestamp without time zone,
    instructor_name character varying(255),
    price double precision NOT NULL,
    capacity integer NOT NULL,
    image_path character varying(255),
    class_type character varying(255),
    yoga_level character varying(255),
    bike_type character varying(255)
);


ALTER TABLE public.fitness_classes OWNER TO "user";

--
-- Name: fitness_classes_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.fitness_classes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.fitness_classes_id_seq OWNER TO "user";

--
-- Name: fitness_classes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.fitness_classes_id_seq OWNED BY public.fitness_classes.id;


--
-- Name: user_classes; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.user_classes (
    id integer NOT NULL,
    user_id integer NOT NULL,
    class_id integer NOT NULL,
    signup_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    paid boolean DEFAULT false
);


ALTER TABLE public.user_classes OWNER TO "user";

--
-- Name: user_classes_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.user_classes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_classes_id_seq OWNER TO "user";

--
-- Name: user_classes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.user_classes_id_seq OWNED BY public.user_classes.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    name character varying(255),
    email character varying(255),
    advertisement boolean DEFAULT false,
    avatar_path character varying(255)
);


ALTER TABLE public.users OWNER TO "user";

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO "user";

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: fitness_classes id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.fitness_classes ALTER COLUMN id SET DEFAULT nextval('public.fitness_classes_id_seq'::regclass);


--
-- Name: user_classes id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.user_classes ALTER COLUMN id SET DEFAULT nextval('public.user_classes_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: fitness_classes; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.fitness_classes (id, name, description, start_time, end_time, instructor_name, price, capacity, image_path, class_type, yoga_level, bike_type) FROM stdin;
4	Power Yoga	Dynamic yoga session focused on strength and stamina.	2025-06-04 10:00:00	2025-06-04 11:00:00	Sofia Reyes	13.5	18	images/power_yoga.jpg	yoga	Intermediate	\N
1	HIIT Blast	High intensity interval training.	2025-06-01 08:00:00	2025-06-01 09:00:00	Alex Smith	15	20	images/hiit.jpg	fitness	\N	\N
3	Spin It Up	Cardio cycling workout.	2025-06-03 18:00:00	2025-06-03 19:00:00	John Doe	14	25	images/spin.jpg	spinning	\N	Mountain Bike
24	Prenatal Yoga	Safe and supportive yoga practice for expectant mothers.	2025-11-29 11:00:00	2025-11-29 12:00:00	Emma Liu	14	10	images/prenatal_yoga.jpg	yoga	All Levels	\N
18	Hill Climb Challenge	Simulate steep climbs and build leg strength with this high-resistance ride.	2025-11-19 06:30:00	2025-11-19 07:15:00	Tom Hardy	17	20	images/leg_workout.jpg	spinning	\N	Road Bike Simulation
23	Tabata Burn	The ultimate HIIT workout: 20 seconds of all-out effort followed by 10 seconds of rest.	2025-11-28 07:00:00	2025-11-28 07:45:00	Alex Smith	18	20	images/hiit.jpg	fitness	\N	\N
14	Core Fusion	An intense workout focused on sculpting your abs, obliques, and lower back.	2025-11-14 08:30:00	2025-11-14 09:15:00	Ben Carter	15.5	16	images/core_workout.jpg	fitness	\N	\N
10	Total Body Blast	A challenging workout that targets all major muscle groups.	2025-11-10 12:00:00	2025-11-10 12:50:00	Alex Smith	17.5	18	images/hiit.jpg	fitness	\N	\N
9	Endurance Cycle	A steady-paced ride designed to improve cardiovascular endurance.	2025-11-08 07:00:00	2025-11-08 08:00:00	Mike Wheeler	15	22	images/spin.jpg	spinning	\N	Stationary
19	Weekend Warrior Bootcamp	A high-intensity mix of cardio and strength drills to kickstart your weekend.	2025-11-22 10:00:00	2025-11-22 11:00:00	Sarah Connor	19	25	images/hiit.jpg	fitness	\N	\N
20	Hatha Yoga Foundation	Focus on classic postures and breathing techniques. Great for beginners.	2025-11-24 10:30:00	2025-11-24 11:30:00	Sofia Reyes	12.5	18	images/yoga.jpg	yoga	Beginner	\N
22	Express Spin	A quick and intense 30-minute ride to fit into your busy schedule.	2025-11-26 12:15:00	2025-11-26 12:45:00	Jessica Lee	10	20	images/spin.jpg	spinning	\N	Stationary
11	Restorative Yoga	A gentle, relaxing class using props to support the body and calm the mind.	2025-11-11 20:00:00	2025-11-11 21:15:00	Priya Patel	15	15	images/yoga.jpg	yoga	Beginner	\N
13	Rhythm Ride	A high-energy, music-driven indoor cycling experience.	2025-11-13 19:00:00	2025-11-13 19:45:00	Jessica Lee	16	25	images/spin.jpg	spinning	\N	Rhythm Bike
15	Ashtanga Primary Series	A powerful, set-sequence practice for experienced yogis.	2025-11-15 09:00:00	2025-11-15 10:30:00	Kenji Tanaka	22	12	images/advanced_yoga.jpg	yoga	Advanced	\N
\.


--
-- Data for Name: user_classes; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.user_classes (id, user_id, class_id, signup_time, paid) FROM stdin;
19	8	1	2025-10-14 11:08:58.810856	t
20	8	3	2025-10-14 11:08:59.583152	t
23	8	4	2025-10-15 15:36:21.288739	t
27	18	4	2025-10-15 16:28:24.038124	t
29	18	1	2025-10-15 16:28:26.213584	t
30	18	3	2025-10-15 16:34:48.830374	t
31	18	24	2025-10-15 16:34:49.743515	t
32	18	18	2025-10-15 16:34:50.647949	t
34	18	14	2025-10-17 08:10:22.806284	t
39	8	23	2025-10-17 11:44:52.578099	t
40	8	24	2025-10-17 11:47:05.875353	t
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.users (id, username, password, name, email, advertisement, avatar_path) FROM stdin;
8	hanna	123456	Hanna Novakova	hanna@gmail.com	t	\N
11	ha	123456	Hanna	123@gmail.com	f	\N
14	John	123456	John doe	john@gmail.com	f	\N
15	john1	123456	John1 doe	john1@gmail.com	f	\N
18	user123	123456	User	user@gmail.com	f	\N
\.


--
-- Name: fitness_classes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.fitness_classes_id_seq', 30, true);


--
-- Name: user_classes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.user_classes_id_seq', 40, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.users_id_seq', 18, true);


--
-- Name: fitness_classes fitness_classes_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.fitness_classes
    ADD CONSTRAINT fitness_classes_pkey PRIMARY KEY (id);


--
-- Name: user_classes user_classes_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.user_classes
    ADD CONSTRAINT user_classes_pkey PRIMARY KEY (id);


--
-- Name: user_classes user_classes_user_id_class_id_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.user_classes
    ADD CONSTRAINT user_classes_user_id_class_id_key UNIQUE (user_id, class_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: user_classes user_classes_class_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.user_classes
    ADD CONSTRAINT user_classes_class_id_fkey FOREIGN KEY (class_id) REFERENCES public.fitness_classes(id) ON DELETE CASCADE;


--
-- Name: user_classes user_classes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.user_classes
    ADD CONSTRAINT user_classes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

