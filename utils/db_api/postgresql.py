from typing import Union

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.ip,
            database=config.DATABASE
        )
        self.pool = pool

    async def create_table_products(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Products (
            id SERIAL PRIMARY KEY,
            file_id VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            description VARCHAR(2000),
            price INT NOT NULL
            );"""
        await self.pool.execute(sql)

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            invited_users_ids VARCHAR(1000),
            bonuses INTEGER DEFAULT 0,
            balance INTEGER DEFAULT 0
            );"""
        await self.pool.execute(sql)

    async def create_table_purchase(self):
        sql = """
        CREATE TABLE IF NOT EXISTS purchase(
            purchase_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            amount INTEGER NOT NULL,
            sum_paid INTEGER NOT NULL,
            adress VARCHAR (255),
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            );"""
        await self.pool.execute(sql)

    async def add_product_to_db(self, file_id: str, url: str, name: str, description: str, price: int):
        sql = """
        INSERT INTO Products(file_id, url, name, description,price) VALUES($1, $2, $3, $4, $5)
        """
        await self.pool.execute(sql, file_id, url, name, description, price)


    async def add_purchase_to_db(self, user_id, product_id, amount, sum_paid, adress):
        sql = """
        INSERT INTO purchase(user_id, product_id, amount, sum_paid, adress) VALUES($1, $2, $3, $4, $5)
        """
        await self.pool.execute(sql, user_id, product_id, amount, sum_paid, adress)


    async def search_like(self, text: str):  # TODO understand how to protect from SQL injection
        text.lower()
        text = f'{text}%'
        sql = f"""
        SELECT * FROM products WHERE LOWER(name) LIKE $1 OR LOWER(description) LIKE $1 ORDER BY name;
        """
        return await self.pool.fetch(sql, text)

    async def get_item_by_id(self, id: int):  # TODO understand how to protect from SQL injection
        sql = f"""
        SELECT * FROM products WHERE id=$1;
        """

        return await self.pool.fetch(sql, id)

    async def add_user(self, id: int):
        sql = """
        INSERT INTO users(user_id) VALUES($1)
        """
        await self.pool.execute(sql, id)

    async def check_user(self, id: int):
        sql = f"""
        select exists(select 1 from users where user_id = $1);
        """
        return await self.pool.fetch(sql, id)

    async def add_bonus(self, user_id: int, amount: int):
        sql = f"""UPDATE users SET bonuses = bonuses + $1 WHERE user_id = $2;"""
        return await self.pool.execute(sql, amount, user_id)


    async def get_bonuses(self, user_id):
        sql = f"""SELECT bonuses FROM users WHERE user_id = $1"""
        return await self.pool.fetch(sql, user_id)

    async def get_all_users(self):
        sql = f"""
        SELECT user_id FROM users;
        """
        return await self.pool.fetch(sql)
