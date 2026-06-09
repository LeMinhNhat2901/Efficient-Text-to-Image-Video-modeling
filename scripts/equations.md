# Equations

```tex
\mathbf{x}_0 \rightarrow \mathbf{x}_T \sim \mathcal{N}(\mathbf{0},\mathbf{I})
```

```tex
dX_t=-\lambda X_t\,dt+\sigma\,dW_t
```

```tex
p(x_t\mid x_{t-1},x_{t-2},\ldots,x_0)=p(x_t\mid x_{t-1})
```

```tex
p(x_{0:T})=p(x_0)\prod_{t=1}^{T}p(x_t\mid x_{t-1})
```

```tex
p(x_{t-1}\mid x_t)=
\frac{p(x_t\mid x_{t-1})p(x_{t-1})}{p(x_t)}
```

```tex
p_\theta(x_{t-1}\mid x_t)=
\mathcal{N}\left(
\mu_\theta(x_t,t),
\Sigma_\theta(x_t,t)
\right)
```
