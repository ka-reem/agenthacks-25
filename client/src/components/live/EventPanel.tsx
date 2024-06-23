import React from 'react';
import { Search, AlertTriangle, AlertCircle, ShieldCheck } from 'lucide-react';
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"

const emergencies = [
  { id: 1, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'CRITICAL' },
  { id: 2, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'CRITICAL' },
  { id: 3, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'MODERATE' },
  { id: 4, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'MODERATE' },
  { id: 5, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'MODERATE' },
  { id: 6, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'MODERATE' },
  { id: 7, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'SAFE' },
  { id: 8, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'SAFE' },
  { id: 9, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'SAFE' },
  { id: 10, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'SAFE' },
  { id: 11, title: 'House Fire in Blair Hills', time: '10:31AM', status: 'SAFE' },
];

const EventPanel = () => {
  return (
    <div className="h-full max-w-md mx-auto p-4 bg-white shadow-lg rounded-lg rounded-none">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold">Emergencies</h2>
        <span className="text-gray-500">Alerts</span>
      </div>
      
      <div className="relative mb-4">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={20} />
        <Input className="pl-10" placeholder="Search a location" />
        <span className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">Filter</span>
      </div>
      
      <div className="flex justify-between mb-4">
        <div>
          <div className="text-2xl font-bold">123</div>
          <div className="text-sm text-gray-500">Total</div>
        </div>
        <div>
          <div className="text-2xl font-bold">34</div>
          <div className="text-sm text-gray-500">Critical</div>
        </div>
        <div>
          <div className="text-2xl font-bold">12</div>
          <div className="text-sm text-gray-500">Resolved</div>
        </div>
      </div>
      
      <div className="space-y-2">
        {emergencies.map((emergency) => (
          <Card key={emergency.id} className="flex items-center p-3">
            {emergency.status === 'CRITICAL' && <AlertCircle className="mr-3 text-red-500" size={24} />}
            {emergency.status === 'MODERATE' && <AlertTriangle className="mr-3 text-orange-500" size={24} />}
            {emergency.status === 'SAFE' && <ShieldCheck className="mr-3 text-green-500" size={24} />}
            <CardContent className="p-0 flex-grow">
              <div className="font-semibold">{emergency.title}</div>
              <div className="text-sm text-gray-500">{emergency.time}</div>
            </CardContent>
            <Badge 
              variant={emergency.status === 'CRITICAL' ? 'destructive' : 
                       emergency.status === 'MODERATE' ? 'secondary' : 'default'}
              className="ml-2"
            >
              {emergency.status}
            </Badge>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default EventPanel;