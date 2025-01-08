import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../UI/Card';
import { MapPin, Phone, Mail } from 'lucide-react';
import Button from '../UI/Button';
import { contactAPI } from '../services/api';

function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  const [status, setStatus] = useState({ type: '', message: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      setStatus({ type: 'loading', message: 'Sending message...' });
      await contactAPI.sendMessage(formData);
      setStatus({ type: 'success', message: 'Message sent successfully!' });
      setFormData({ name: '', email: '', message: '' });
    } catch (error) {
      setStatus({ 
        type: 'error', 
        message: error.response?.data?.detail || 'Failed to send message' 
      });
    }
  };

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Contact Us</h1>
      <div className="grid md:grid-cols-2 gap-8">
        {/* Contact Form Card */}
        <Card>
          <CardHeader>
            <CardTitle>Send us a Message</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full p-2 border rounded-md"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full p-2 border rounded-md"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Message</label>
                <textarea
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  className="w-full p-2 border rounded-md h-32"
                  required
                />
              </div>
              {status.message && (
                <div className={`p-2 rounded ${
                  status.type === 'error' ? 'bg-red-100 text-red-700' :
                  status.type === 'success' ? 'bg-green-100 text-green-700' :
                  'bg-blue-100 text-blue-700'
                }`}>
                  {status.message}
                </div>
              )}
              <Button 
                type="submit" 
                className="w-full"
                disabled={status.type === 'loading'}
              >
                {status.type === 'loading' ? 'Sending...' : 'Send Message'}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Contact Information Cards */}
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <MapPin className="w-5 h-5 mr-2" />
                Location
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>123 Racing Street</p>
              <p>Racing City, RC 12345</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Phone className="w-5 h-5 mr-2" />
                Phone
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>+1 (555) 123-4567</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Mail className="w-5 h-5 mr-2" />
                Email
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p>info@racingcenter.com</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

export default Contact;