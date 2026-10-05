# 🔎 AI-Powered Intelligent Lost & Found Matching and Recovery System

An AI-powered web application that helps users find and recover lost items by intelligently matching lost and found item records using images, descriptions, and locations.

## 📌 Problem Statement

Traditional lost and found systems mainly depend on manually checking item descriptions or contacting authorities. This can be time-consuming and may make it difficult to identify a matching item quickly.

This project provides an intelligent system that automatically compares lost and found items and generates a match score.

## 💡 Proposed Solution

The system uses AI-based image similarity along with description and location matching to identify potentially matching lost and found items.

Users can:

- Report a lost item
- Report a found item
- Upload item images
- Provide item descriptions
- Provide location details
- Add contact information
- View AI-generated match scores
- Check match confidence
- Claim a possible matching item
- View recovery/contact details

## 🚀 Key Features

### 🔴 Lost Item Registration
Users can register lost items with:

- Item name
- Description
- Location
- Image
- Contact information

### 📦 Found Item Registration
Users can register found items with the same information.

### 🤖 AI-Powered Matching

The system compares lost and found items using:

- 🖼️ Image similarity
- 📝 Description similarity
- 📍 Location similarity

### 🏆 Match Score

The system calculates an overall match score and displays the matching confidence.

- 🟢 80%+ → Strong Match
- 🟡 60–79% → Possible Match
- 🔴 50–59% → Low Match

### 🤝 Claim / Contact

When a possible match is found, users can view the recovery details and finder contact information.

### 📊 Dashboard

The dashboard displays:

- Number of lost items
- Number of found items
- AI matching status

## 🧠 AI Matching Method

The project uses CLIP through Sentence Transformers for image and text embeddings.

The overall matching score combines:

```text
Overall Score =
Image Similarity × 60%
+ Description Similarity × 30%
+ Location Similarity × 10%