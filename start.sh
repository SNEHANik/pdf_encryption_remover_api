#!/bin/bash
uvicorn pdf_parsing_api:app --host 0.0.0.0 --port $PORT
