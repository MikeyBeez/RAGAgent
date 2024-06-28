graph TD
    subgraph Head
        A["🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦"]
        B["🔵        ████████          ████████       🔵"]
        C["🟠        ██    ██          ██    ██       🟠"]
        D["🟢        ██  * ██    TT    ██ *  ██       🟢"]
        E["🟣        ██    ██          ██    ██       🟣"]
        F["🔴        ████████          ████████       🔴"]
        G["🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦🟦"]
    end
    
    subgraph Heart
        H["❤️              ❤️   ❤️             ❤️"]
        I[" ❤️   ❤️                      ❤️   ❤️"]
        J["  ❤️          ❤️       ❤️         ❤️"]
        K["   ❤️              ❤️            ❤️"]
        L["     ❤️                         ❤️"]
        M["       ❤️                     ❤️"]
        N["         ❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️"]
    end
    
    subgraph Base
        O["🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨"]
        P["🟨🟨🟨🟨🟨🟨🟨🟨🟨🟨"]
    end
    
    A --> B --> C --> D --> E --> F --> G
    G --> H --> I --> J --> K --> L --> M --> N
    N --> O --> P

    style A fill:#4444FF,stroke:#4444FF
    style G fill:#4444FF,stroke:#4444FF
    style O fill:#FFFF00,stroke:#FFFF00
    style P fill:#FFFF00,stroke:#FFFF00
