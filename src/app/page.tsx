import { Card, Title, Text } from '@tremor/react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', headcount: 120 },
  { month: 'Feb', headcount: 125 },
  { month: 'Mar', headcount: 130 },
  { month: 'Apr', headcount: 128 },
  { month: 'May', headcount: 135 },
];

const kpis = [
  { label: 'Total Employees', value: '1,234' },
  { label: 'New Hires (YTD)', value: '45' },
  { label: 'Attrition Rate', value: '3.2%' },
  { label: 'Avg. Tenure', value: '4.5 yrs' },
];

export default function Home() {
  return (
    <div className="p-6 space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((kpi, index) => (
          <div key={index} className="kpi-card">
            <div className="kpi-label">{kpi.label}</div>
            <div className="kpi-value">{kpi.value}</div>
          </div>
        ))}
      </div>

      <Card>
        <Title>Headcount Trend</Title>
        <Text>Monthly employee headcount over time</Text>
        <div className="h-72 mt-4">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Area 
                type="monotone" 
                dataKey="headcount" 
                stroke="#3b82f6" 
                fill="#93c5fd" 
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  )
}