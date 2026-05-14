# Mihomo 配置模板整理

这个目录保留本地历史配置，但 Git 只追踪脱敏后的 `*Template.yaml` 和说明文档。
模板中的机场订阅统一使用占位符，不在仓库中保存真实订阅链接。

## 模板选择

- `Company99-Config-FakeIP-Template.yaml`：推荐主模板。保留 Fake-IP，并用 `nameserver-policy` 对交易所、AI、GFW、GitHub、Google、Telegram 等敏感域名指定可信 DoH。适合更重视 DNS 污染规避和规则精细度的场景。
- `Company99-Config-FakeIP-FilterOnly-Template.yaml`：保守基础模板。保留 Fake-IP 的过滤名单，但不主动对敏感域名做 `nameserver-policy` 分流。适合优先稳定、少改 DNS 行为的场景。
- `Company-Config-FakeIP-Template.yaml`：Company 版本模板。整体与 Company99 策略版接近，但代理提供者命名和 Akilo 节点组更少。
- `Ho-Config-FakeIP-Template.yaml`：Ho 基准模板。开启 IPv6，保留 `find-process-mode: off`，代理分组同步 Company99 结构，但不引入 company 专用 rule-provider。

## 本地使用方式

1. 复制一个 `*Template.yaml` 为本地实际配置文件。
2. 将 `proxy-providers` 里的 `#❗provider占位N` 替换成自己的机场订阅 provider。
3. 将 `use-all-proxy-providers` 里的 `#❗use-provider占位N` 替换成对应 provider 名称。
4. 本地实际配置文件不要改名为 `*Template.yaml`，避免被 Git 追踪。

示例：

```yaml
proxy-providers:
  provider1:
    <<: *proxy-providers-general
    override:
      additional-prefix: "provider1|"
    url: "你的机场订阅链接"
    path: ./providers/proxy/provider1.yaml

use-all-proxy-providers: &use-all-proxy-providers
  use:
    - provider1
```

## 直接使用注意

1. 当前模板文件不能直接作为可用订阅导入，因为真实 provider 仍需要由订阅生成工具或本地配置注入。
2. 直接本地使用时，需要先按“本地使用方式”替换占位符。
3. `template-placeholder` 只用于让模板在未注入订阅时保持合法结构，方便 `mihomo -t` 校验；实际使用时应由订阅生成工具或本地配置注入真实 provider。
4. 本地实际配置文件不要改名为 `*Template.yaml`，避免被 Git 追踪。

## 隐私规则

- `.gitignore` 默认忽略所有 `.yaml`。
- 仅允许提交 `*Template.yaml`。
- 模板里的订阅地址只保留 provider/use 占位符，不提交真实订阅链接。
