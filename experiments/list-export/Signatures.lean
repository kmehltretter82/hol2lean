import Init

/- Independent targets for the export experiment. Each definition is a proposition
   against which a future imported declaration can be type-checked. -/
namespace Hol2Lean.Fixture

universe u

def appendNil : Prop :=
  ∀ (α : Type u) [Nonempty α] (xs : List α), xs ++ [] = xs

def appendAssoc : Prop :=
  ∀ (α : Type u) [Nonempty α] (xs ys zs : List α),
    xs ++ (ys ++ zs) = (xs ++ ys) ++ zs

def reverseAppend : Prop :=
  ∀ (α : Type u) [Nonempty α] (xs ys : List α),
    (xs ++ ys).reverse = ys.reverse ++ xs.reverse

end Hol2Lean.Fixture
