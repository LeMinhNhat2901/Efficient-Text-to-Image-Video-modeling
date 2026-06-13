# References & Further Reading

This repository is heavily inspired by the rapidly evolving field of generative modeling, specifically text-to-image architectures, diffusion models, and discrete latent transformers. Below is an extensive list of the foundational papers, mathematical texts, and articles that influenced the scripts, code, and visual animations in these videos.

## 1. Score-based Models & Stochastic Differential Equations (SDEs)
*The mathematical backbone explored in Video 1.*

- **Song, Y., Sohl-Dickstein, J., Kingma, D. P., Kumar, A., Ermon, S., & Poole, B. (2020).** *Score-Based Generative Modeling through Stochastic Differential Equations.* ICLR 2021. This is the definitive text on unifying score-based models and diffusion using continuous-time SDEs, the Fokker-Planck equation, and Probability Flow ODEs.
- **Ho, J., Jain, A., & Abbeel, P. (2020).** *Denoising Diffusion Probabilistic Models (DDPM).* NeurIPS 2020. Introduced the standard parameterization of discrete-time diffusion.
- **Song, Y., & Ermon, S. (2019).** *Generative Modeling by Estimating Gradients of the Data Distribution.* NeurIPS 2019. The foundation for score matching and Langevin dynamics in generative AI.
- **Sohl-Dickstein, J., Weiss, E., Maheswaranathan, N., & Ganguli, S. (2015).** *Deep Unsupervised Learning using Nonequilibrium Thermodynamics.* ICML 2015. The original paper that introduced diffusion models.
- **Anderson, B. D. (1982).** *Reverse-time diffusion equation models.* Stochastic Processes and their Applications. The core theorem proving the existence of the reverse SDE.
- **Hyvärinen, A. (2005).** *Estimation of Non-Normalized Statistical Models by Score Matching.* Journal of Machine Learning Research (JMLR). The origin of score matching.
- **Vincent, P. (2011).** *A Connection Between Score Matching and Denoising Autoencoders.* Neural Computation. Proved that denoising score matching is equivalent to estimating the score of the data distribution.

## 2. Discrete Generative Models & Tokenization
*The concepts covered in the first half of Video 2 (VQGAN, Masked Generative Models).*

- **Esser, P., Rombach, R., & Ommer, B. (2021).** *Taming Transformers for High-Resolution Image Synthesis (VQGAN).* CVPR 2021. Introduced the concept of treating images as discrete "visual words" via a learned codebook.
- **Van Den Oord, A., Vinyals, O., et al. (2017).** *Neural Discrete Representation Learning (VQ-VAE).* NeurIPS 2017. The precursor to VQGAN, introducing vector quantization in neural networks.
- **Chang, H., Zhang, H., Barber, J., Maschinot, A., Lezama, J., Jiang, L., ... & Freeman, W. T. (2023).** *Muse: Text-To-Image Generation via Masked Generative Transformers.* ICML 2023. Demonstrated that parallel decoding of masked visual tokens can rival or beat continuous diffusion in speed.
- **Yu, J., Li, X., Koh, J. Y., Zhang, H., Pang, R., Qin, J., ... & Wu, Y. (2022).** *Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti).* arXiv. Massive scaling of discrete autoregressive image generation.

## 3. Latent Diffusion & Architecture Evolution
*The transition to latent spaces and DiT architectures.*

- **Rombach, R., Blattmann, A., Lorenz, D., Esser, P., & Ommer, B. (2022).** *High-Resolution Image Synthesis with Latent Diffusion Models (LDM).* CVPR 2022. The architecture behind Stable Diffusion, combining perceptual compression with diffusion models.
- **Peebles, W., & Xie, S. (2023).** *Scalable Diffusion Models with Transformers (DiT).* ICCV 2023. Proved that UNet architectures can be entirely replaced by Vision Transformers (ViT) operating on latent patches.
- **Zhao, Z., et al. (2024).** *Sana: Efficient High-Resolution Image Synthesis with Linear Diffusion.* The latest innovations in compressing text embeddings (Gemma) and applying linear attention (Mamba/Linear Transformers) to achieve ultra-fast, high-quality generation.
- **Bao, F., Li, C., Zhu, J., & Zhang, M. (2023).** *All are Worth Words: A ViT Paradigm for Visual Generation (U-ViT).* CVPR 2023. Another early exploration of transformer-based diffusion.

## 4. Guidance & Alignment
*How we steer the diffusion process (Classifier-Free Guidance).*

- **Ho, J., & Salimans, T. (2022).** *Classifier-Free Diffusion Guidance.* NeurIPS 2022 Workshop. The revolutionary technique that allows text-to-image models to follow prompts accurately without needing a separate classifier.
- **Dhariwal, P., & Nichol, A. (2021).** *Diffusion Models Beat GANs on Image Synthesis.* NeurIPS 2021. Introduced Classifier Guidance using gradients from a pre-trained noisy image classifier.
- **Radford, A., Kim, J. W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., ... & Sutskever, I. (2021).** *Learning Transferable Visual Models From Natural Language Supervision (CLIP).* ICML 2021. The critical multimodal alignment model that gives text prompts their meaning in visual space.

## 5. Text-to-Image Milestones
*The historic models that paved the way.*

- **Ramesh, A., Pavlov, M., Goh, G., Gray, S., Voss, C., Radford, A., ... & Sutskever, I. (2021).** *Zero-Shot Text-to-Image Generation (DALL-E).* ICML 2021. The first massive autoregressive text-to-image model.
- **Ramesh, A., Dhariwal, P., Nichol, A., Chu, C., & Chen, M. (2022).** *Hierarchical Text-Conditional Image Generation with CLIP Latents (DALL-E 2).* arXiv. Introduced diffusion priors and CLIP embeddings for generation.
- **Saharia, C., Chan, W., Saxena, S., Li, L., Whang, J., Denton, E., ... & Norouzi, M. (2022).** *Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding (Imagen).* NeurIPS 2022. Showed that large frozen text encoders (T5) are excellent for diffusion model conditioning.

## 6. General Machine Learning & Mathematics
*Books and resources for building the underlying mathematical intuition.*

- **Särkkä, S., & Solin, A. (2019).** *Applied Stochastic Differential Equations.* Cambridge University Press. Excellent resource for understanding Itô calculus, the Fokker-Planck equation, and numerical solvers (Runge-Kutta).
- **Goodfellow, I., Bengio, Y., & Courville, A. (2016).** *Deep Learning.* MIT Press. The foundational text for understanding optimization, neural networks, and generative models (GANs, VAEs).
- **Bishop, C. M. (2006).** *Pattern Recognition and Machine Learning.* Springer. Foundational text for probability distributions and Markov chains.
- **Oksendal, B. (2013).** *Stochastic Differential Equations: An Introduction with Applications.* Springer Science & Business Media. Deep dive into the rigorous math behind SDEs.

## 7. Software & Visualization Tools

- **Manim (Math Animation Framework)**: 3D and 2D mathematical animations used extensively to visualize score functions and vectors.
- **PyTorch**: The core deep learning framework utilized by almost all referenced papers.
- **Hugging Face Diffusers**: Simplifies the implementation of SDE solvers and continuous-time sampling equations.
