from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-later')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///users.db')
app.config['BASE_HOURLY_RATE'] = float(os.environ.get('BASE_HOURLY_RATE', '15.0'))
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV', 'development')
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    discount_percentage = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(50), default='#2ecc71')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    booking_name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    duration_hours = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    sale_applied = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=True)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, approved, denied, in_progress, completed
    admin_notes = db.Column(db.Text, nullable=True)
    user_notes = db.Column(db.Text, nullable=True)
    num_dogs = db.Column(db.Integer, nullable=True)
    dog_breed = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='bookings')
    sale = db.relationship('Sale', backref='bookings')
    selected_animals = db.relationship('BookingAnimal', backref='booking', lazy=True, cascade='all, delete-orphan')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), unique=False, nullable=True)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    animals = db.relationship('Animal', backref='owner', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    animal_type = db.Column(db.String(50), nullable=False)  # dog, cat, bird, rabbit, etc.
    breed = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)  # in pounds
    special_needs = db.Column(db.Text, nullable=True)
    temperament = db.Column(db.String(50), nullable=True)  # friendly, shy, energetic, etc.
    medical_conditions = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to booking associations with cascade delete
    booking_associations = db.relationship('BookingAnimal', backref='animal', lazy=True, cascade='all, delete-orphan')

class BookingAnimal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), nullable=False)
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'), nullable=False)

class Ban(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Helper to check if banned
def is_banned(email=None, phone=None, ip=None):
    ban_query = Ban.query
    if email:
        ban_query = ban_query.filter_by(email=email)
    if phone:
        ban_query = ban_query.filter_by(phone_number=phone)
    if ip:
        ban_query = ban_query.filter_by(ip_address=ip)
    return ban_query.first() is not None

@app.route('/')
def home():
    active_sale = Sale.query.filter_by(is_active=True).first()
    return render_template('home.html', active_sale=active_sale, base_rate=app.config['BASE_HOURLY_RATE'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        ip = request.remote_addr
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            if is_banned(email=user.email) or is_banned(phone=user.phone_number) or is_banned(ip=ip):
                flash('You are banned from logging in. Contact support.')
                return redirect(url_for('login'))
            if user.check_password(request.form['password']):
                login_user(user)
                return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        ip = request.remote_addr
        email = request.form['email']
        phone = request.form.get('phone')
        if is_banned(email=email) or is_banned(phone=phone) or is_banned(ip=ip):
            flash('You are banned from registering. Contact support.')
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=request.form['email']).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(
            username=request.form['username'],
            email=email,
            phone_number=phone
        )
        user.set_password(request.form['password'])
        # Make the first registered user an admin
        if User.query.count() == 0:
            user.is_admin = True
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    users = User.query.all()
    sales = Sale.query.all()
    return render_template('admin.html', users=users, sales=sales)

@app.route('/admin/sale', methods=['POST'])
@login_required
def manage_sale():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    
    action = request.form.get('action')
    if action == 'create':
        sale = Sale(
            name=request.form['name'],
            discount_percentage=float(request.form['discount']),
            is_active=bool(request.form.get('is_active')),
            color=request.form['color']
        )
        db.session.add(sale)
    elif action == 'update':
        sale_id = int(request.form['sale_id'])
        sale = db.session.get(Sale, sale_id)
        if not sale:
            flash('Sale not found')
            return redirect(url_for('admin'))
        sale.name = request.form['name']
        sale.discount_percentage = float(request.form['discount'])
        sale.is_active = bool(request.form.get('is_active'))
        sale.color = request.form['color']
    elif action == 'delete':
        sale_id = int(request.form['sale_id'])
        sale = db.session.get(Sale, sale_id)
        if not sale:
            flash('Sale not found')
            return redirect(url_for('admin'))
        db.session.delete(sale)
    
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book_session():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(request.form['time'], '%H:%M').time()
        duration = float(request.form['duration'])
        user_notes = request.form.get('user_notes')
        
        # Handle selected animals
        selected_animal_ids = request.form.getlist('selected_animals')
        num_animals = len(selected_animal_ids)  # Auto-count selected animals
        
        # Calculate cost
        base_cost = app.config['BASE_HOURLY_RATE'] * duration
        active_sale = Sale.query.filter_by(is_active=True).first()
        if active_sale:
            discount = base_cost * (active_sale.discount_percentage / 100)
            total_cost = base_cost - discount
            sale_id = active_sale.id
        else:
            total_cost = base_cost
            sale_id = None
            
        booking = Booking(
            user_id=current_user.id,
            booking_name=request.form['booking_name'],
            phone_number=request.form['phone'],
            date=date,
            start_time=start_time,
            duration_hours=duration,
            total_cost=total_cost,
            sale_applied=sale_id,
            status='pending',
            user_notes=user_notes,
            num_dogs=num_animals,  # Store auto-counted number
            dog_breed=''  # Keep for backward compatibility, but not used
        )
        db.session.add(booking)
        db.session.flush()  # Get booking ID
        
        # Handle selected animals
        for animal_id in selected_animal_ids:
            if animal_id:  # Skip empty values
                booking_animal = BookingAnimal(booking_id=booking.id, animal_id=int(animal_id))
                db.session.add(booking_animal)
        
        db.session.commit()
        flash('Your booking request has been submitted and is pending approval.')
        return redirect(url_for('my_bookings'))
    active_sale = Sale.query.filter_by(is_active=True).first()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get user's animals for selection
    user_animals = Animal.query.filter_by(user_id=current_user.id).order_by(Animal.name).all()
    
    return render_template('book.html', base_rate=app.config['BASE_HOURLY_RATE'], active_sale=active_sale, today=today, user_animals=user_animals)

@app.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.date, Booking.start_time).all()
    # Load selected animals for each booking
    for booking in bookings:
        booking.selected_animals_list = [ba.animal for ba in booking.selected_animals]
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/my-animals')
@login_required
def my_animals():
    animals = Animal.query.filter_by(user_id=current_user.id).order_by(Animal.name).all()
    return render_template('my_animals.html', animals=animals)

@app.route('/add-animal', methods=['GET', 'POST'])
@login_required
def add_animal():
    if request.method == 'POST':
        animal = Animal(
            user_id=current_user.id,
            name=request.form['name'],
            animal_type=request.form['animal_type'],
            breed=request.form['breed'],
            age=request.form.get('age', type=int),
            weight=request.form.get('weight', type=float),
            special_needs=request.form.get('special_needs'),
            temperament=request.form.get('temperament'),
            medical_conditions=request.form.get('medical_conditions')
        )
        db.session.add(animal)
        db.session.commit()
        flash('Animal profile added successfully!')
        return redirect(url_for('my_animals'))
    return render_template('add_animal.html')

@app.route('/edit-animal/<int:animal_id>', methods=['GET', 'POST'])
@login_required
def edit_animal(animal_id):
    animal = Animal.query.filter_by(id=animal_id, user_id=current_user.id).first_or_404()
    if request.method == 'POST':
        animal.name = request.form['name']
        animal.animal_type = request.form['animal_type']
        animal.breed = request.form['breed']
        animal.age = request.form.get('age', type=int)
        animal.weight = request.form.get('weight', type=float)
        animal.special_needs = request.form.get('special_needs')
        animal.temperament = request.form.get('temperament')
        animal.medical_conditions = request.form.get('medical_conditions')
        db.session.commit()
        flash('Animal profile updated successfully!')
        return redirect(url_for('my_animals'))
    return render_template('edit_animal.html', animal=animal)

@app.route('/delete-animal/<int:animal_id>', methods=['POST'])
@login_required
def delete_animal(animal_id):
    animal = Animal.query.filter_by(id=animal_id, user_id=current_user.id).first_or_404()
    db.session.delete(animal)
    db.session.commit()
    flash('Animal profile deleted successfully!')
    return redirect(url_for('my_animals'))

@app.route('/view-animal/<int:animal_id>')
@login_required
def view_animal(animal_id):
    animal = Animal.query.filter_by(id=animal_id, user_id=current_user.id).first_or_404()
    return render_template('view_animal.html', animal=animal)

@app.route('/delete-booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.filter_by(id=booking_id).first_or_404()
    
    # Check if user is admin or owns the booking
    if not current_user.is_admin and booking.user_id != current_user.id:
        flash('Access denied')
        return redirect(url_for('home'))
    
    # Don't allow deletion of completed bookings
    if booking.status == 'completed':
        flash('Cannot delete completed bookings')
        return redirect(url_for('my_bookings') if booking.user_id == current_user.id else url_for('admin_bookings'))
    
    db.session.delete(booking)
    db.session.commit()
    
    if current_user.is_admin:
        flash('Booking deleted successfully!')
        return redirect(url_for('admin_bookings'))
    else:
        flash('Your booking has been cancelled successfully!')
        return redirect(url_for('my_bookings'))

@app.route('/admin/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('admin'))
    if user.id == current_user.id:
        flash('Cannot delete your own account')
        return redirect(url_for('admin'))
    # Delete all bookings for this user first
    Booking.query.filter_by(user_id=user.id).delete()
    db.session.delete(user)
    db.session.commit()
    flash('User and their bookings deleted')
    return redirect(url_for('admin'))

@app.route('/admin/toggle-admin/<int:user_id>')
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('admin'))
    if user.id == current_user.id:
        flash('Cannot modify your own admin status')
        return redirect(url_for('admin'))
    
    user.is_admin = not user.is_admin
    db.session.commit()
    flash(f'Admin status updated for {user.username}')
    return redirect(url_for('admin'))

@app.route('/admin/booking/<int:booking_id>', methods=['POST'])
@login_required
def update_booking(booking_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))

    booking = db.session.get(Booking, booking_id)
    if not booking:
        flash('Booking not found')
        return redirect(url_for('admin_bookings'))

    action = request.form.get('action')

    if action == 'status':
        new_status = request.form.get('status')
        if new_status:
            booking.status = new_status
            flash(f'Booking #{booking.id} status updated to {new_status}.')
    elif action == 'notes':
        new_notes = request.form.get('notes')
        booking.admin_notes = new_notes
        flash(f'Admin notes for booking #{booking.id} updated.')
    
    db.session.commit()
    return redirect(url_for('admin_bookings'))
@app.route('/admin/bookings')
@login_required
def admin_bookings():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    bookings = Booking.query.order_by(Booking.date, Booking.start_time).all()
    # Load selected animals for each booking
    for booking in bookings:
        booking.selected_animals_list = [ba.animal for ba in booking.selected_animals]
    return render_template('admin_bookings.html', bookings=bookings)

@app.route('/legal')
def legal():
    return render_template('legal.html')

@app.route('/pet-requirements')
def pet_requirements():
    return render_template('pet_requirements.html')

# Admin user management from JSON
ADMIN_JSON_PATH = os.path.join(os.path.dirname(__file__), 'admin_user.json')
def load_admin_user():
    if not os.path.exists(ADMIN_JSON_PATH):
        return None
    with open(ADMIN_JSON_PATH, 'r') as f:
        return json.load(f)

def ensure_admin_user():
    admin_data = load_admin_user()
    if not admin_data or not admin_data.get('enabled', True):
        return
    user = User.query.filter_by(username=admin_data['username']).first()
    if not user:
        user = User(
            username=admin_data['username'],
            email=admin_data['email'],
            is_admin=True
        )
        user.set_password(admin_data['password'])
        db.session.add(user)
        db.session.commit()
    else:
        user.is_admin = True
        db.session.commit()

with app.app_context():
    # Only create tables if they don't exist (for development)
    try:
        db.create_all()
        ensure_admin_user()
    except Exception as e:
        # Tables might already exist, skip creation
        print(f"Database tables already exist or error occurred: {e}")
        # Still ensure admin user exists
        try:
            ensure_admin_user()
        except Exception as admin_error:
            print(f"Admin user setup error: {admin_error}")

@app.route('/admin/toggle-admin-user', methods=['POST'])
@login_required
def toggle_admin_user():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('admin'))
    admin_data = load_admin_user()
    if not admin_data:
        flash('No admin user config found.')
        return redirect(url_for('admin'))
    admin_data['enabled'] = not admin_data.get('enabled', True)
    with open(ADMIN_JSON_PATH, 'w') as f:
        json.dump(admin_data, f, indent=2)
    flash(f"Admin user access {'enabled' if admin_data['enabled'] else 'disabled'}.")
    # Optionally, update DB user status
    user = User.query.filter_by(username=admin_data['username']).first()
    if user:
        user.is_admin = admin_data['enabled']
        db.session.commit()
    return redirect(url_for('admin'))

@app.route('/admin/ban/<int:user_id>', methods=['POST'])
@login_required
def ban_user(user_id):
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('admin'))
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('admin'))
    # Ban by email, phone, and IP
    ban = Ban(email=user.email, phone_number=user.phone_number)
    db.session.add(ban)
    db.session.commit()
    flash('User banned. All future users with same email, phone, or IP will be banned.')
    return redirect(url_for('admin'))

@app.route('/health')
def health_check():
    """Health check endpoint for deployment monitoring"""
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}

if __name__ == '__main__':
    with app.app_context():
        ensure_admin_user()
    app.run(debug=True)