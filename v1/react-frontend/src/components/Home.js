import { Link } from 'react-router-dom';
import './Home.css';
import Header from "./Header"
import rsvp from "./assets/rsvp.png"
import eventImage from "./assets/create-event.png"
import invitImage from './assets/send-invitation.png'


const Home = () => {
    return (
        <div className="home">
            <Header />
            <header className="home-header">
                <h1>Welcome to Our Event Management System</h1>
                <p>Your one-stop solution for managing and organizing events.</p>
                <p>Manage guests, send invitations, and track RSVPs with ease.</p>
                <Link  to="/register"> <button className='btn-account'>Create new account</button></Link>
            </header>
                    <h2>Features:</h2>
            <section className="home-content">
                <div className="feature">
                    <h2>Manage Events</h2>
                    <p>Organize and keep track of all your events in one place.</p>
                    <Link to="/admin/events" className="btn">Learn more</Link>
                </div>
                <div className="feature">
                    <h2>Track Attendees</h2>
                    <p>Monitor and manage attendees effortlessly.</p>
                    <Link to="/admin/users" className="btn">Learn more</Link>
                </div>
                <div className="feature">
                    <h2>Generate Reports</h2>
                    <p>Get detailed insights and reports on your events.</p>
                    <Link to="/admin/reports" className="btn">Learn more</Link>
                </div>
                <div className="feature">
                    <h2>RSVP Tracking</h2>
                    <p>Track guest responses easily</p>
                    <Link to="/admin/settings" className="btn">Learn more</Link>
                </div>
            </section>
            <section class="testimonials">
                <div className='body'>
        <h1>What Our Clients Are Saying</h1>
        <p>See how our event invitations management has helped make events unforgettable.</p>

        <div class="testimonial-card">
            <div class="testimonial-text">
                <p>"The invitation management system was a game changer for our event. It streamlined the process, allowed for beautiful customization, and our guests loved the ease of RSVPing. I couldn't be happier with the service!"</p>
            </div>
            <div class="testimonial-info">
                <div>
                    <strong>Sarah Thompson</strong>
                    <p>Event Coordinator, Gala Events</p>
                </div>
            </div>
        </div>

        <div class="testimonial-card">
            <div class="testimonial-text">
                <p>"Organizing our annual conference was a breeze with this tool. The automation of invitations and follow-ups saved us so much time and the analytics were incredibly helpful for managing attendee engagement."</p>
            </div>
            <div class="testimonial-info">
                <div>
                    <strong>Michael Lee</strong>
                    <p>Conference Manager, TechSummit</p>
                </div>
            </div>
        </div>

        <div class="testimonial-card">
            <div class="testimonial-info">
            <div class="testimonial-text">
                <p>"From sending invitations to tracking responses, everything was handled effortlessly. The customizable templates were a hit, and our event was a huge success thanks to this amazing service."</p>
            </div>
                <div>
                    <strong>Emily Carter</strong>
                    <p>Wedding Planner</p>
                </div>
            </div>
        </div>
                    
                </div>
    </section>
    <section class="how-it-works">
        <h1>How It Works</h1>
        <p>Follow these simple steps to manage your event invitations seamlessly.</p>

        <div class="steps">
            <div class="step">
                {/* <img src={eventImage} alt="Create Event Screenshot" class="step-image"></img> */}
                <div class="step-content">
                    <h2>0. Create an account</h2>
                    <p>Create a new accout or login if you have an existing account</p>
                </div>
            </div>
            <div class="step">
                <img src={eventImage} alt="Create Event Screenshot" class="step-image"></img>
                <div class="step-content">
                    <h2>1. Create Event</h2>
                    <p>Start by setting up your event with all the details. Customize your event page and choose from a variety of templates.</p>
                </div>
            </div>

            <div class="step">
                <img src={rsvp} alt="Manage Guests Screenshot" class="step-image"></img>
                <div class="step-content">
                    <h2>2. Manage Guests</h2>
                    <p>Effortlessly manage your guest list. Add, edit, or remove guests and organize them into groups for targeted communication.</p>
                </div>
            </div>

            <div class="step">
                <img src={invitImage} alt="Send Invitation Screenshot" class="step-image"></img>
                <div class="step-content">
                    <h2>3. Send Invitations</h2>
                    <p>Send beautifully designed invitations via email or social media. Personalize each message and track delivery status.</p>
                </div>
            </div>

            <div class="step">
                <img src={rsvp} alt="Track RSVP Screenshot" class="step-image"></img>
                <div class="step-content">
                    <h2>4. Track RSVPs</h2>
                    <p>Monitor RSVP responses in real-time. Get detailed reports on who has accepted or declined, and manage follow-ups as needed.</p>
                </div>
            </div>
        </div>
        <div>
            <button className='btn-demo'>Request Demo</button>
        </div>
    </section>
        </div>
    );
};

export default Home;
