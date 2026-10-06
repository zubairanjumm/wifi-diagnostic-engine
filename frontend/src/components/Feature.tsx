interface FeatureProps {
  number: string
  title: string
  description: string
}

export function Feature({
  number,
  title,
  description,
}: FeatureProps) {
  return (
    <article className="feature-card">
      <span className="feature-number">{number}</span>
      <h3 className="mt-6 text-xl font-semibold tracking-[-0.02em] text-white">
        {title}
      </h3>
      <p className="mt-3 text-sm leading-7 text-slate-400">
        {description}
      </p>
    </article>
  )
}
