from django.urls import reverse
from rest_framework import status
from datetime import date
from rest_framework.test import APITestCase
from users_transactions.models import User, Transaction


class UserTests(APITestCase):
    def test_create_user(self):
        """
        Ensure we can create a new User object.
        """
        url = "/users/"
        data = {"name": "Dan Cooper", "age": 32, "email": "d_b_cooper@gmail.com"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().id, 1)
        self.assertEqual(User.objects.get().name, "Dan Cooper")
        self.assertEqual(User.objects.get().age, 32)
        self.assertEqual(User.objects.get().email, "d_b_cooper@gmail.com")

    def test_retrieve_user(self):
        """
        Ensure we can retrieve a User object details on response.
        """
        self.test_create_user()

        url = "/users/1/"
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("id"), 1)
        self.assertEqual(response.json().get("name"), "Dan Cooper")
        self.assertEqual(response.json().get("age"), 32)
        self.assertEqual(response.json().get("email"), "d_b_cooper@gmail.com")

    def test_update_user(self):
        """
        Ensure we can update User details.
        """
        self.test_create_user()

        url = "/users/1/"
        data = {"name": "New Name", "age": 99, "email": "new_mail@gmail.com"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("id"), 1)
        self.assertEqual(response.json().get("name"), "New Name")
        self.assertEqual(response.json().get("age"), 99)
        self.assertEqual(response.json().get("email"), "new_mail@gmail.com")

    def test_destroy_user(self):
        """
        Ensure we can destroy a User object.
        """
        self.test_create_user()

        url = "/users/1/"
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TransactionsTests(APITestCase):
    def test_create_transaction(self):
        """
        Ensure we can create a new Transaction object.
        """
        UserTests.test_create_user(self)
        url = "/transactions/"
        data = {
            "reference": "000001",
            "account": "C00099",
            "date": "2020-01-03",
            "amount": -51.13,
            "type": "outflow",
            "category": "rent",
            "user_id": 1,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().reference, "000001")
        self.assertEqual(Transaction.objects.get().account, "C00099")
        self.assertEqual(Transaction.objects.get().date, date(2020, 1, 3))
        self.assertEqual(Transaction.objects.get().type, "outflow")
        self.assertEqual(Transaction.objects.get().category, "rent")
