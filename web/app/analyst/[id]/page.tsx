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
    <main>
      <h1>{analyst?.display_name}</h1>
      <p>Win Rate: {analyst?.win_rate?.toFixed(1) ?? "-"}%</p>
      <p>Tahmin Sayısı: {analyst?.sample_size ?? "-"}</p>
      <h2>Tahminler</h2>
    
      <ul>
        {predictions?.map((prediction) => (
          <li key={prediction.id}>
            {prediction.asset} {prediction.direction} → hedef {prediction.target_price}, stop {prediction.stop_price} — <strong>{prediction.status}</strong>
          </li>
        ))}
      </ul>

        <h2>Performans Grafiği</h2>
        <Chart data={statusCounts} />
    </main>
  );
}