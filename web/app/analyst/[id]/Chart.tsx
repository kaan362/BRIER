'use client'

import { BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts'


export default function Chart({ data }: { data: { name: string; count: number }[] }) {
  return (
    <BarChart width={400} height={250} data={data}>
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="count" fill="#4f46e5" />
    </BarChart>
  );
}