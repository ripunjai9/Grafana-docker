from helpers import Helpers
import pymysql
import os
from dotenv import dotenv_values


class GrafanaDb:
    def __init__(self):
        self._helpers = Helpers()
        self.env = self._helpers.get_env_path()

    def __connect(self):
        try:
            host_name = self.env['GRAFANA_DB_HOSTNAME']
            user = self.env['GRAFANA_DB_USER']
            password = self.env['GRAFANA_DB_PASSWORD']
            db_name = self.env['GRAFANA_DB_NAME']
            db_conn = pymysql.connect(
                db=db_name, user=user,
                passwd=password, host=host_name)
            return db_conn
        except Exception as e:
            print("Grafana Database Connection Error:", str(e))

    def is_session_valid(self, auth_key, ip_address, user_login_id, user_login_detail, is_ip_checked):
        if is_ip_checked:
            sql = """
                    SELECT COUNT(*) 
                    FROM user_auth_token at,user s 
                    WHERE s.id=at.user_id  
                        AND (at.auth_token=%s or at.prev_auth_token=%s) 
                        AND at.client_ip=%s 
                        AND s.id=%s 
                        AND s.login=%s;
                    """
            params = (
                auth_key, auth_key, ip_address, user_login_id, user_login_detail,
            )
        else:
            sql = """
                    SELECT COUNT(*) 
                    FROM user_auth_token at, user s 
                    WHERE s.id=at.user_id 
                        AND (at.auth_token=%s OR at.prev_auth_token=%s) 
                        AND s.id=%s 
                        AND s.login=%s;
                    """
            params = (auth_key, auth_key, user_login_id, user_login_detail,)
        try:
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql, params)
            rows = _cursor.fetchall()
            count = 0
            for row in rows:
                count = row[0]

            return (count is not None and int(count) > 0)
        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to validate Session: :" + str(ex))
            return False
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    # Tenancy
    def get_organizations(self):
        sql = "SELECT name FROM poly_organization"
        try:
            organizations = []
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql)
            rows = _cursor.fetchall()
            for row in rows:
                organizations.append(row[0])
            return organizations
        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to get user organizations: " + str(ex))
            return None
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def remove_organisations_deleted_in_sciencelogic(self, data_list):
        organizations = [item for sublist in data_list for item in sublist]
        sql = "SELECT name FROM poly_organization WHERE name NOT IN %s "
        params = (organizations,)
        try:
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql, params)
            rows = _cursor.fetchall()
            unmapped_organizations = []
            for row in rows:
                unmapped_organizations.append(row[0])

            if len(unmapped_organizations) > 0:
                query = """
                        DELETE FROM poly_user_organization 
                        WHERE organization_id IN (
                            SELECT id 
                            FROM poly_organization
                            WHERE name IN %s
                        ) """
                _cursor.execute(query, (unmapped_organizations,))
                db_conn.commit()

                query = """
                        DELETE FROM poly_organization 
                        WHERE name IN %s """
                _cursor.execute(query, (unmapped_organizations,))
                db_conn.commit()

        except Exception as ex:
            print(sql.replace("\n", " "))
            print(
                "Error: unable to remove ScienceLogic deleted organisations from grafana DB:" + str(ex))
            return None
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def insert_organizations(self, organizations):
        if organizations is None or len(organizations) == 0:
            return None

        sql = "INSERT INTO poly_organization (name) VALUES  "
        for organization in organizations:
            sql += "('" + str(organization[0]) + "'),"
        sql = sql[:-1]
        try:
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql)
            db_conn.commit()
        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to adding user organisations:" + str(ex))
            return None
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def get_users(self):
        sql = "SELECT email FROM poly_users "
        try:
            users = []
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql)
            rows = _cursor.fetchall()
            for row in rows:
                users.append(row[0])
            return users
        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to get poly grafana users: " + str(ex))
            return None
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def insert_users(self, emails):
        if emails is None or len(emails) == 0:
            return None

        sql = "INSERT INTO poly_users (email) VALUES  "
        for email in emails:
            sql += "('" + str(email) + "'),"
        sql = sql[:-1]
        try:
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql)
            db_conn.commit()
        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to insert poly grafana users:" + str(ex))
            return None
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def remove_azure_deleted_user_email(self, emails):
        sql = "SELECT email FROM poly_users WHERE email NOT IN %s "
        params = (emails,)
        try:
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql, params)
            rows = _cursor.fetchall()
            unmapped_users_email = []
            for row in rows:
                unmapped_users_email.append(row[0])

            if len(unmapped_users_email) > 0:
                # Delete FK mapping from SQL DB
                query = """
                        DELETE FROM poly_user_organization 
                        WHERE user_id IN (
                            SELECT id 
                            FROM poly_users 
                            WHERE email IN %s
                        ) """
                _cursor.execute(query, (unmapped_users_email,))
                db_conn.commit()
                # Deleting the records from DB
                query = "DELETE FROM poly_users WHERE email IN %s "
                _cursor.execute(query, (unmapped_users_email,))
                db_conn.commit()
        except Exception as ex:
            print(sql.replace("\n", " "))
            print(
                "Error: unable to remove azure deleted user email from grafana DB:" + str(ex))
            return None
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def get_poly_user_organization_list(self):
        sql = """
                SELECT po.name, pu.email 
                FROM poly_users pu, 
                    poly_organization po, 
                    poly_user_organization puo
                WHERE pu.id=puo.user_id 
                    AND po.id=puo.organization_id
                """
        try:
            poly_user_organizations = []
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql)
            poly_user_organization = _cursor.fetchall()
            poly_user_organization_dictionary = {}
            for row in poly_user_organization:
                organization = row[0]
                email = row[1]
                if poly_user_organization_dictionary.get(email) is None:
                    poly_user_organization_dictionary[email] = [
                        organization]
                    poly_user_organizations.append(
                        poly_user_organization_dictionary)
                else:
                    poly_user_organization_dictionary.get(
                        email).append(organization)
            print(poly_user_organization_dictionary)
            return poly_user_organization_dictionary
        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to get poly grafana users: " + str(ex))
            return None
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def add_organization_to_user(self, organization, user_email):
        sql = """
            SELECT 
                DISTINCT pu.id, po.id 
            FROM   
                poly_users pu, poly_organization po
            WHERE
                po.name in %s 
                AND pu.email= %s
            """
        params = (organization, user_email)
        try:
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql, params)
            rows = _cursor.fetchall()
            insert_sql = """INSERT 
                            INTO poly_user_organization (user_id, organization_id) 
                            VALUES  """
            if rows is not None and len(rows) > 0:
                for row in rows:
                    user_id = row[0]
                    organization_id = row[1]
                    insert_sql += "(" + str(user_id) + "," + \
                        str(organization_id) + "),"
                insert_sql = insert_sql[:-1]

                # Delete FK mapping from poly_user_organization
                delete_sql = """DELETE 
                                FROM poly_user_organization 
                                WHERE user_id = (
                                    SELECT id 
                                    FROM poly_users
                                    WHERE email = %s
                                ) """
                _cursor.execute(delete_sql, (user_email,))
                db_conn.commit()
                _cursor.execute(insert_sql)
                db_conn.commit()
                
                # Delete duplicate record mapping from poly_user_organization
                delete_duplicates_sql = """DELETE c1 
                                FROM poly_user_organization c1 
                                INNER JOIN poly_user_organization c2 
                                WHERE  c1.id > c2.id 
                                    AND  c1.organization_id = c2.organization_id 
                                    AND  c1.user_id = c2.user_id """
                _cursor.execute(delete_duplicates_sql)
                db_conn.commit()

                return "Organization added successfully", "success"

        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to add poly user and organization to the DB:" + str(ex))
            return "Error: unable to add poly user and organization to the DB:", "failure"
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def get_user_organization(self, email):
        sql = """
            SELECT 
                po.name 
            FROM  
                poly_users pu, 
                poly_organization po, 
                poly_user_organization pug  
            WHERE 
                pu.id=pug.user_id 
                AND po.id=pug.organization_id 
                AND pu.email = %s """
        try:
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            _cursor.execute(sql, email)
            rows = _cursor.fetchall()
            user_organizations = []
            if rows is not None and len(rows) > 0:
                for row in rows:
                    organization = row[0]
                    user_organizations.append(organization)
            return user_organizations
        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to get poly users organization: " + str(ex))
            return None
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()

    def update_user_organisations(self, organizations):
        if organizations is None or len(organizations) == 0:
            raise Exception(
                "Failed while updating grafana user organization due to empty data list from SL DB."
            )
        try:
            user_organizations = self.get_organizations()
            if user_organizations is None or len(user_organizations) == 0:
                self.insert_organizations(organizations)
            else:
                new_organizations = []
                for organization in organizations:
                    organization = organization[0]
                    if organization not in user_organizations:
                        new_organizations.append([organization])
                if len(new_organizations) > 0:
                    self.insert_organizations(new_organizations)
                self.remove_organisations_deleted_in_sciencelogic(
                    organizations)
        except Exception as e:
            print(e)

    def update_users(self, poly_azure_emails):
        if poly_azure_emails is None or len(poly_azure_emails) == 0:
            raise Exception(
                "Failed while updating grafana user due to empty user list from Microsoft AD."
            )
        try:
            users = self.get_users()
            if users is None or len(users) == 0:
                self.insert_users(
                    poly_azure_emails)
            else:
                new_user_list = []
                for email in poly_azure_emails:
                    if email not in users:
                        new_user_list.append(email)
                if len(new_user_list) > 0:
                    self.insert_users(new_user_list)
                self.remove_azure_deleted_user_email(
                    poly_azure_emails)
        except Exception as e:
            print(e)
