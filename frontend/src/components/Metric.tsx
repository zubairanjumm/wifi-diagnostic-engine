interface MetricProps {
  label: string
  value: string
}

export function Metric({
  label,
  value,
}: MetricProps) {
  return (
    <div className="rounded-xl border border-black/10 bg-white p-5">
      <p className="text-xs font-medium uppercase tracking-wider text-black/40">
        {label}
      </p>

      <p className="mt-2 text-xl font-semibold tracking-tight">
        {value}
      </p>
    </div>
  )
}