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
    <div className="border-t border-black/10 pt-5">
      <span className="text-xs font-medium text-black/40">
        {number}
      </span>

      <h3 className="mt-4 text-lg font-semibold">
        {title}
      </h3>

      <p className="mt-2 text-sm leading-6 text-black/55">
        {description}
      </p>
    </div>
  )
}