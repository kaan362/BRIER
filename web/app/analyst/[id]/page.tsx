import { supabase } from '../../../lib/supabase'
import Chart from './Chart'

export default async function AnalystCard({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params

  const { data: predictions, error } = await supabase
    .from('predictions')
    .select('*, outcomes(*)')
    .eq('analyst_id', id)

  const statusCounts = ["hit", "stopped", "expired", "pending"].map((status) => ({
    name: status,
    count: predictions?.filter((p) => p.status === status).length ?? 0,
  }))

  const { data: analyst } = await supabase
    .from('analysts')
    .select('*')
    .eq('id', id)
    .single()

  return (
    
    <main className="max-w-2xl mx-auto p-8">
      {error && (
        <p className="text-red-600 mb-4">Mistake occurred while loading data.</p>
      )}
      <h1 className="text-2xl font-bold mb-2">{analyst?.display_name}</h1>
      <p className="text-gray-600">Win Rate: {analyst?.win_rate?.toFixed(1) ?? "-"}%</p>
      <p className="text-gray-600 mb-6">Sample Size: {analyst?.sample_size ?? "-"}</p>

      <h2 className="text-xl font-semibold mb-3">Predictions</h2>
     {predictions && predictions.length > 0 ? (
        <ul className="mb-8">
          {predictions.map((prediction) => (
            <li key={prediction.id} className="border-b py-2">
              {prediction.asset} {prediction.direction} → target {prediction.target_price}, stop {prediction.stop_price} — <strong>{prediction.status}</strong>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-gray-500 mb-8">No predictions available.</p>
      )}

      <h2 className="text-xl font-semibold mb-3">Performance Graph</h2>
      <Chart data={statusCounts} />
    </main>
  );
}