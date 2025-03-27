import unittest
from unittest import mock
import os
import boto3
import botocore

# Set environment variables for AWS credentials (to avoid real credential lookup)
os.environ['AWS_ACCESS_KEY_ID'] = 'fake-access'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'fake-secret'

# Import functions to be tested from the apod_pipeline module
from dags.pipelines.apod_pipeline import extract, transform, apod_pipeline

class TestNasaETL(unittest.TestCase):
    """
    Test suite for testing the ETL (Extract, Transform, Load) process in the NASA APOD pipeline.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class-wide resources and mock external dependencies before any test.
        """
        # Mock the `make_api_call` method to avoid real API calls during testing
        cls.patcher_make_api_call = mock.patch("dags.pipelines.apod_pipeline.make_api_call", new=mock.MagicMock())
        cls.patcher_make_api_call.start()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after all tests are completed.
        """
        cls.patcher_make_api_call.stop()

    def setUp(self):
        """
        Set up per-test resources and mock external dependencies for each individual test.
        """
        # Mock the `make_api_call` method in the general_functions module
        self.patcher_make_api_call = mock.patch("dags.utils.general_functions.make_api_call", new=mock.MagicMock())
        self.mock_make_api_call = self.patcher_make_api_call.start()
        self.addCleanup(self.patcher_make_api_call.stop)

        # Mock the `make_api_call` method for APOD pipeline
        self.patcher_apod_make_api_call = mock.patch("dags.pipelines.apod_pipeline.make_api_call", new=mock.MagicMock())
        self.mock_apod_make_api_call = self.patcher_apod_make_api_call.start()
        self.addCleanup(self.patcher_apod_make_api_call.stop)

        # Mock the `save_data_locally` method to return a fake file path
        self.expected_file_path = 'fake_path.csv'
        self.patcher_save_data_locally = mock.patch('dags.pipelines.apod_pipeline.save_data_locally', return_value=self.expected_file_path)
        self.mock_save_data_locally = self.patcher_save_data_locally.start()
        self.addCleanup(self.patcher_save_data_locally.stop)

        # Mock the `extract` method to avoid actual API calls
        self.patcher_apod_extract = mock.patch('dags.pipelines.apod_pipeline.extract')
        self.mock_apod_extract = self.patcher_apod_extract.start()
        self.addCleanup(self.patcher_apod_extract.stop)

        # Mock the `load` method (for loading data to a destination)
        self.patcher_apod_load = mock.patch('dags.pipelines.apod_pipeline.load')
        self.mock_apod_load = self.patcher_apod_load.start()
        self.addCleanup(self.patcher_apod_load.stop)
        
        # Mock the `transform` method (data transformation step)
        self.patcher_apod_transform = mock.patch('dags.pipelines.apod_pipeline.transform')
        self.mock_apod_transform = self.patcher_apod_transform.start()
        self.addCleanup(self.patcher_apod_transform.stop)

    def test_make_api_call_was_called(self):
        """
        Test that the `make_api_call` method is called once when `extract` is executed.
        """
        extract()  # This should trigger the mocked `make_api_call`
        self.mock_apod_make_api_call.assert_called_once()  # Check that it was called exactly once

    def test_path_is_returned(self):
        """
        Test that the `transform` method correctly returns the file path.
        """
        actual_file_path = transform()  # Call the transform method, which internally calls save_data_locally
        self.assertEqual(actual_file_path, self.expected_file_path)  # Assert the returned path is as expected

    def test_nested_functions_are_called(self):
        """
        Test that nested functions (transform, load) are called during the execution of the full pipeline.
        """
        apod_pipeline()  # Run the full pipeline (extract -> transform -> load)
        self.mock_apod_transform.assert_called()  # Ensure the transform method was called
        self.mock_apod_load.assert_called()  # Ensure the load method was called

# Run the tests if this file is executed directly
if __name__ == '__main__':
    unittest.main()
