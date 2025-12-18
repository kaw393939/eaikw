# CMS Comparison: Sanity vs Strapi vs Contentful

| Category              | **Sanity**                                                                 | **Strapi**                                                                 | **Contentful**                                                                 |
|-----------------------|-----------------------------------------------------------------------------|-----------------------------------------------------------------------------|--------------------------------------------------------------------------------|
| **Data Modeling**     | Schema-as-code (JS/TS). Highly flexible, modular, version-controlled.       | GUI or code-defined content types. Supports components & relations.         | GUI-driven content types. Structured but less flexible for developers.          |
| **API / Querying**    | GROQ (expressive, JSON-like), GraphQL, REST via client. CDN-backed queries. | REST + GraphQL APIs. Performance depends on hosting.                        | REST + GraphQL APIs. Global CDN ensures fast delivery.                          |
| **Developer Experience** | Schema-as-code integrates with Git/CI/CD. Customizable Studio (React). Strong docs. | Node.js-based, open-source. Extensible with plugins/hooks. Balanced GUI + code. | Polished APIs/SDKs. GUI-driven schema. Strong ecosystem, less dev control.      |
| **Editorial Workflow**| Real-time collaborative Studio. Fully customizable UI. Flexible workflows.  | Functional admin panel. Role-based access. Less polished collaboration.     | Highly polished UI. Roles, workflows, approvals, localization.                  |
| **Pricing & Limits**  | Generous free tier (20 seats). Usage-based scaling. Predictable costs.      | Free if self-hosted. Cloud pricing affordable but limited API/storage.      | Free tier limited. Paid plans start high (~$300/mo). Enterprise-focused.        |
| **Integration w/ Eleventy** | Official starters + plugins. Seamless GROQ/GraphQL integration. Fast builds. | Works via REST/GraphQL. Requires custom fetch logic.                        | Works via REST/GraphQL. Documented examples exist, but no official starter.     |
| **Fit for This Project** | Best balance: schema-as-code, Eleventy integration, SEO/accessibility fields, cost-effective. | Good for dev-heavy teams who want open-source control. More setup overhead. | Strong editorial workflows, but higher cost and less developer flexibility.     |

# Final Selection & Justification

## 🎯 Final Choice: **Sanity**

After evaluating **Sanity**, **Strapi**, and **Contentful** across all critical categories—data modeling, API/querying, developer experience, editorial workflow, pricing & limits, integration with Eleventy, and overall project fit—**Sanity emerges as the most effective CMS for this project**.

---

## 🔎 Justification with Examples

### 1. Data Modeling

- **Sanity** uses **schema-as-code**, allowing developers to define content structures in JavaScript/TypeScript.  
- This aligns perfectly with our modular, version-controlled workflow.  
- Example: Unlike **Contentful's GUI-driven modeling**, Sanity lets us embed accessibility metadata and SEO fields directly into schemas, ensuring compliance and flexibility.

### 2. API / Querying

- **Sanity's GROQ query language** is expressive and tailored for content, with GraphQL support as well.  
- Queries are resolved at the CDN edge, ensuring **fast builds with Eleventy**.  
- Example: **Strapi** requires custom fetch logic, while **Contentful** offers GraphQL but less schema control. Sanity's GROQ makes complex queries simple and efficient.

### 3. Developer Experience

- **Sanity Studio** is React-based and fully customizable, fitting seamlessly into modern workflows (Git, CI/CD).  
- Example: Developers can version schemas alongside code, unlike **Contentful's GUI-only schema**, which limits flexibility.  
- **Strapi** offers extensibility but requires heavier setup and maintenance.

### 4. Editorial Workflow

- **Sanity Studio** supports **real-time collaboration**, similar to Google Docs, and can be tailored to editorial needs.  
- Example: Editors can preview content live, while **Strapi's admin panel** is functional but less polished, and **Contentful's UI**, though polished, lacks customization.

### 5. Pricing & Limits

- **Sanity** provides a generous free tier (20 seats, unlimited content types) and predictable usage-based scaling.  
- Example: **Contentful's paid plans start at ~$300/month**, making it expensive for smaller teams.  
- **Strapi** is free if self-hosted but requires infrastructure management. Sanity balances cost-effectiveness with scalability.

### 6. Integration with Eleventy

- **Sanity** offers **official Eleventy starters and plugins**, making integration seamless.  
- Example: **Strapi** and **Contentful** both require custom API fetches, while Sanity's GROQ queries plug directly into Eleventy's data pipeline.

### 7. Fit for THIS Project

- Our project emphasizes **modularity, SEO, accessibility, and performance**.  
- **Sanity** excels here:
  - Schema-as-code supports modular workflows.  
  - SEO fields and accessibility metadata can be embedded directly.  
  - CDN-backed queries ensure performance goals (Core Web Vitals).  
- Example: **Contentful** shines in editorial polish but is costly and less flexible for developers. **Strapi** is strong for open-source control but requires more setup overhead. Sanity balances both worlds.

---

## 🏆 Conclusion

**Sanity wins because it provides the best balance of developer control, editorial collaboration, Eleventy integration, and cost-effectiveness.**  

- Developers benefit from schema-as-code and GROQ queries.  
- Editors gain real-time collaboration in a customizable Studio.  
- The project gains predictable pricing, strong SEO/accessibility support, and seamless Eleventy integration.  

Sanity is not just the most effective CMS—it is the **best fit for THIS project's goals of modularity, performance, and future-proof workflows**.
