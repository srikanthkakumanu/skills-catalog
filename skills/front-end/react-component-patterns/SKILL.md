---
name: react-component-patterns
description: >
  Use when designing or reviewing React 19 component APIs — prop design, composition, compound
  components, ref handling, or component-to-component data flow. Covers compound components,
  explicit variant props over boolean-prop explosion, children-over-render-props, React 19's
  ref-as-a-prop (no forwardRef), and context interface design.
---

# React Component Patterns (React 19)

## Explicit Variants, Not Boolean-Prop Explosion

A component's prop surface should express its states as one closed set, not an independent boolean
per state. Booleans compose combinatorially — `isPrimary` + `isDanger` + `isLarge` allows nonsense
combinations (`isPrimary={true} isDanger={true}`) the type system can't reject.

```tsx
// Bad — boolean props allow invalid combinations and don't scale
type ButtonProps = {
  isPrimary?: boolean;
  isDanger?: boolean;
  isLarge?: boolean;
  isSmall?: boolean;
};

// Good — one closed variant prop; invalid states are unrepresentable
type ButtonProps = {
  variant: 'primary' | 'secondary' | 'danger';
  size: 'sm' | 'md' | 'lg';
};

function Button({ variant, size, ...props }: ButtonProps & React.ComponentProps<'button'>) {
  return <button className={buttonVariants({ variant, size })} {...props} />;
}
```

## Compound Components for Related UI

When several components share implicit state (a `Tabs` list and its panels, an `Accordion` and its
items), expose that relationship through a shared context rather than prop-drilling every child's
configuration through the parent.

```tsx
type TabsContextValue = { activeTab: string; setActiveTab: (id: string) => void };
const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error('Tabs.* must be rendered inside <Tabs>');
  return ctx;
}

function Tabs({ defaultTab, children }: { defaultTab: string; children: React.ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  return (
    <TabsContext.Provider value={{ activeTab, setActiveTab }}>{children}</TabsContext.Provider>
  );
}

Tabs.Trigger = function TabsTrigger({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab, setActiveTab } = useTabsContext();
  return (
    <button aria-selected={activeTab === id} onClick={() => setActiveTab(id)}>
      {children}
    </button>
  );
};

Tabs.Panel = function TabsPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeTab } = useTabsContext();
  return activeTab === id ? <div role="tabpanel">{children}</div> : null;
};
```

A ready-to-copy starter is in `templates/CompoundComponent.tsx`.

## Children Over Render Props

Prefer `children` for simple content injection; reach for a render-prop/function-as-child only when
the child genuinely needs data the parent computed (e.g. a measured size, a fetched item).

```tsx
// Unnecessary — plain children would do
<DataList render={(items) => items.map((i) => <Item key={i.id} {...i} />)} />

// Better — children is enough when there's nothing to hand back
<DataList>
  <Item />
</DataList>
```

## ref as a Plain Prop (React 19)

React 19 passes `ref` through to function components as an ordinary prop — `forwardRef` is no
longer required for a component that needs to expose a DOM node or imperative handle.

```tsx
// Bad — forwardRef is legacy ceremony in React 19
const Input = forwardRef<HTMLInputElement, InputProps>((props, ref) => (
  <input ref={ref} {...props} />
));

// Good — ref is just a prop
function Input({ ref, ...props }: InputProps & { ref?: React.Ref<HTMLInputElement> }) {
  return <input ref={ref} {...props} />;
}
```

## Small, Decoupled Context Interfaces

A context's value type is a public API — keep it to what consumers actually need, not the entire
internal state shape of the provider. A context that leaks setters and internal flags couples every
consumer to the provider's implementation details.

```tsx
// Bad — leaks the whole internal state shape
const ctx = { state, setState, internalFlag, _debugInfo };

// Good — a narrow, intentional interface
const ctx = { activeTab, selectTab: (id: string) => setState((s) => ({ ...s, activeTab: id })) };
```

## Lift State to the Nearest Common Owner

State used by two sibling components belongs in their nearest common ancestor, not duplicated in
each sibling or hoisted further up than necessary (which widens the re-render blast radius).

## Official sources

- React composition docs: https://react.dev/learn/passing-props-to-a-component
- React 19 ref-as-prop: https://react.dev/blog/2024/12/05/react-19#ref-as-a-prop
- Adapted from Vercel's `composition-patterns` agent skill (compound components, avoid boolean
  props, children over render props, explicit variants, lift state, context interface design):
  https://github.com/vercel-labs/agent-skills

## Gotchas

- Agent adds a new boolean prop for every visual state — collapse into one `variant`/`size` union instead.
- Agent uses `forwardRef` on a new component in a React 19 codebase — pass `ref` as a plain prop.
- Agent prop-drills shared state through 3+ component levels — use a compound-component context instead.
- Agent exposes the entire provider state object through context — narrow it to what consumers need.
- Agent reaches for a render prop where `children` alone would work — prefer `children` unless the child needs computed data back.
- Agent defines a component inside another component's render body — this recreates the component type every render, resetting all child state; define it at module scope.
