export interface MetricItem {
    label: string;
    value: number;
}

export default function MetricGrid( { items }: { items: MetricItem[]}) {
    return (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
            {items.map((item) => (
                <div key={item.label} className="rounded-2xl border bg-white p-5 shadow-sm">
                    <p className="text-sm text-slate-500">{item.label}</p>
                    <p className="mt-2 text-3xl font-bold text-emerald-700">{item.value}</p>
                </div>
            ))}
        </div>
    );
}