import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../UI/Card';
import { MapPin, Phone, Mail } from 'lucide-react';
import Button from '../UI/Button';

function Contact(){
  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-8">Contact Us</h1>
      <div className="grid md:grid-cols-2 gap-8">
        <Card>
          <CardHeader>
            <CardTitle>Send us a Message</CardTitle>
          </CardHeader>
          <CardContent>
            <form className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Name</label>
                <input
                  type="text"
                  className="w-full p-2 border rounded-md"
                  placeholder="Your name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input
                  type="email"
                  className="w-full p-2 border rounded-md"
                  placeholder="your@email.com"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Message</label>
                <textarea
                  className="w-full p-2 border rounded-md h-32"
                  placeholder="Your message"
                />
              </div>
              <Button className="w-full">Send Message</Button>
            </form>
          </CardContent>
        </Card>

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