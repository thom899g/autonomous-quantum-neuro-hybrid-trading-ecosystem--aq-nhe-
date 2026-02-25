"""
Firebase Client for AQ-NHE Ecosystem
Handles all Firestore operations with robust error handling and connection management
"""
import logging
from typing import Any, Dict, List, Optional, Union
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore, exceptions
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.base_query import FieldFilter

from config.settings import config

logger = logging.getLogger(__name__)

class FirebaseClient:
    """Firebase Firestore client with connection pooling and error recovery"""
    
    _instance = None
    _client = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to prevent multiple Firebase instances"""
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Firebase connection if not already initialized"""
        if not self._initialized:
            try:
                self._initialize_firebase()
                self._initialized = True
                logger.info("Firebase client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Firebase: {e}")
                raise
    
    def _initialize_firebase(self) -> None:
        """Initialize Firebase Admin SDK with error handling"""
        try:
            # Check if Firebase app already exists
            if not firebase_admin._apps:
                cred_dict = {
                    "type": "service_account",
                    "project_id": config.firebase.project_id,
                    "private_key_id": config.firebase.private_key_id,
                    "private_key": config.firebase.private_key,
                    "client