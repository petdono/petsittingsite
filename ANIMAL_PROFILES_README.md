# Dog Profiles Feature

This document describes the new dog sub-profiles feature added to the pet sitting website.

## Overview

The dog profiles feature allows users to create detailed profiles for their dogs and select which dogs are involved in each booking. This provides better information to sitters and makes the booking process more personalized.

## Features

### For Users:
- **Create Dog Profiles**: Add detailed information about each dog including name, breed, age, weight, temperament, special needs, and medical conditions
- **Edit Dog Profiles**: Update dog information as needed
- **Delete Dog Profiles**: Remove dog profiles when no longer needed
- **Select Dogs for Bookings**: Choose which dogs will be involved in each booking
- **View Dog Profiles**: See all their dog profiles in one place

### For Admins:
- **Enhanced Booking View**: See detailed information about selected dogs for each booking
- **Special Needs Alerts**: Visual indicators for dogs with special needs
- **Complete Dog Information**: Breed, age, temperament, and medical conditions displayed

## Database Schema

### Dog Table
- `id`: Primary key
- `user_id`: Foreign key to User table
- `name`: Dog's name
- `breed`: Dog's breed
- `age`: Dog's age in years
- `weight`: Dog's weight in pounds
- `special_needs`: Any special care instructions
- `temperament`: Dog's personality (friendly, shy, energetic, etc.)
- `medical_conditions`: Health conditions or medications
- `created_at`: Profile creation timestamp
- `updated_at`: Last update timestamp

### BookingDog Table (Association Table)
- `id`: Primary key
- `booking_id`: Foreign key to Booking table
- `dog_id`: Foreign key to Dog table

## User Interface

### Navigation
- Added "My Dogs" link in the main navigation for authenticated users

### Dog Management Pages
- **My Dogs** (`/my-dogs`): View all dog profiles with edit/delete options
- **Add Dog** (`/add-dog`): Create new dog profiles
- **Edit Dog** (`/edit-dog/<dog_id>`): Modify existing dog profiles

### Booking Process
- **Dog Selection**: When booking, users can select from their dog profiles
- **Visual Cards**: Dog profiles displayed as cards with key information
- **Special Needs Indicators**: Visual alerts for dogs with special needs

### Admin Panel
- **Enhanced Table**: Shows selected dogs with breed, age, and special needs
- **Detailed Information**: Complete dog profiles visible to admins

## Usage Instructions

### Creating Dog Profiles
1. Log in to your account
2. Click "My Dogs" in the navigation
3. Click "Add New Dog"
4. Fill in the dog information
5. Click "Save Dog Profile"

### Using Dog Profiles in Bookings
1. Go to "Book a Session"
2. Fill in booking details
3. In the "Select Dogs" section, check the boxes for dogs involved in this booking
4. Complete the booking process

### Managing Dog Profiles
1. Go to "My Dogs"
2. Use the dropdown menu on each dog card to edit or delete
3. Edit form allows updating all dog information

## Benefits

1. **Better Communication**: Sitters get detailed information about each dog
2. **Personalized Service**: Different care instructions for different dogs
3. **Health Awareness**: Medical conditions and special needs are clearly communicated
4. **Efficient Booking**: No need to re-enter dog information for each booking
5. **Admin Efficiency**: Admins can quickly see which dogs are involved and their requirements

## Technical Implementation

- **Models**: Dog, BookingDog (association table)
- **Routes**: `/my-dogs`, `/add-dog`, `/edit-dog/<dog_id>`, `/delete-dog/<dog_id>`
- **Templates**: `my_dogs.html`, `add_dog.html`, `edit_dog.html`
- **Database Migration**: Script provided to add new tables
- **CSS Styling**: Custom styles for dog selection cards and profile display

## Future Enhancements

- Photo uploads for dog profiles
- Dog behavior history tracking
- Emergency contact information per dog
- Integration with veterinary records
- Dog care schedule templates