PGDMP      $                }            notaconforme    16.2    16.2     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    24687    notaconforme    DATABASE     �   CREATE DATABASE notaconforme WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';
    DROP DATABASE notaconforme;
                postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    24696    usuarios    TABLE     �   CREATE TABLE public.usuarios (
    id bigint NOT NULL,
    nome character varying(300),
    email character varying(300) NOT NULL,
    senha character varying(300) NOT NULL,
    ativo boolean
);
    DROP TABLE public.usuarios;
       public         heap    user_notaconforme    false    4            �            1259    24695    usuarios_id_seq    SEQUENCE     x   CREATE SEQUENCE public.usuarios_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 &   DROP SEQUENCE public.usuarios_id_seq;
       public          user_notaconforme    false    216    4            �           0    0    usuarios_id_seq    SEQUENCE OWNED BY     C   ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;
          public          user_notaconforme    false    215            P           2604    24699    usuarios id    DEFAULT     j   ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);
 :   ALTER TABLE public.usuarios ALTER COLUMN id DROP DEFAULT;
       public          user_notaconforme    false    216    215    216            �          0    24696    usuarios 
   TABLE DATA           A   COPY public.usuarios (id, nome, email, senha, ativo) FROM stdin;
    public          user_notaconforme    false    216   �       �           0    0    usuarios_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.usuarios_id_seq', 2, false);
          public          user_notaconforme    false    215            S           2606    24703    usuarios usuarios_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);
 @   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_pkey;
       public            user_notaconforme    false    216            Q           1259    24709    ix_usuarios_email    INDEX     N   CREATE UNIQUE INDEX ix_usuarios_email ON public.usuarios USING btree (email);
 %   DROP INDEX public.ix_usuarios_email;
       public            user_notaconforme    false    216            �   l   x�3�tL���S��/ITp��K�/�M�L�9�I���\N�$C#��$��(Ss��T����4'/3��7c� ?��$w��(��D�p�2��"/3�4g��=... � K     