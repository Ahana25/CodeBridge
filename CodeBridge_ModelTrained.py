# -*- coding: utf-8 -*-
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
import matplotlib.pyplot as plt
import json
import random
import pickle
import os
from tqdm import tqdm
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)
if torch.cuda.is_available():
    torch.cuda.manual_seed(42)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Device: {device}")

class ImprovedDataGenerator:
    def __init__(self, seed=42):
        random.seed(seed)
        self.entities = [
            'User', 'Payment', 'Order', 'Product', 'Customer', 'Invoice',
            'Cart', 'Transaction', 'Account', 'Session', 'Auth', 'Token',
            'Subscription', 'Notification', 'Email', 'Message', 'Log',
            'Report', 'Analytics', 'Metric', 'Dashboard', 'Widget',
            'Inventory', 'Stock', 'Warehouse', 'Shipment', 'Delivery',
            'Review', 'Rating', 'Comment', 'Feedback', 'Survey',
            'Discount', 'Coupon', 'Promotion', 'Campaign', 'Offer',
            'Category', 'Tag', 'Label', 'Filter', 'Search',
            'Image', 'Video', 'Media', 'Asset', 'File',
            'Permission', 'Role', 'Group', 'Team', 'Organization'
        ]

        self.fields = [
            'id', 'uid', 'uuid', 'email', 'username', 'password', 'hash',
            'amount', 'price', 'cost', 'total', 'subtotal', 'tax', 'fee',
            'status', 'state', 'active', 'enabled', 'visible', 'deleted',
            'name', 'title', 'description', 'content', 'body', 'text',
            'quantity', 'count', 'number', 'size', 'weight', 'volume',
            'timestamp', 'createdAt', 'updatedAt', 'deletedAt', 'expiresAt',
            'userId', 'customerId', 'productId', 'orderId', 'cartId',
            'category', 'type', 'kind', 'variant', 'version', 'revision',
            'rating', 'score', 'points', 'rank', 'priority', 'position',
            'address', 'city', 'country', 'zipcode', 'latitude', 'longitude',
            'phone', 'mobile', 'fax', 'website', 'url', 'endpoint',
            'color', 'style', 'theme', 'template', 'layout', 'format'
        ]

        self.operations = [
            'create', 'read', 'update', 'delete', 'upsert', 'patch',
            'get', 'set', 'fetch', 'load', 'save', 'store',
            'find', 'search', 'filter', 'sort', 'paginate', 'limit',
            'validate', 'verify', 'check', 'confirm', 'approve', 'reject',
            'process', 'handle', 'execute', 'run', 'perform', 'trigger',
            'send', 'receive', 'publish', 'subscribe', 'broadcast', 'emit',
            'connect', 'disconnect', 'bind', 'unbind', 'attach', 'detach',
            'encrypt', 'decrypt', 'hash', 'sign', 'verify', 'authenticate',
            'cache', 'refresh', 'expire', 'invalidate', 'purge', 'clear'
        ]

        self.var_names = ['data', 'item', 'obj', 'entity', 'record', 'doc',
                          'payload', 'request', 'response', 'result', 'output',
                          'input', 'params', 'args', 'config', 'options']

    def generate_javascript(self, count=1000):
        samples = []
        for i in range(count):
            entity = random.choice(self.entities)
            field1 = random.choice(self.fields)
            field2 = random.choice(self.fields)
            operation = random.choice(self.operations)
            var_name = random.choice(self.var_names)

            patterns = [
                f"""async function {operation}{entity}({var_name}) {{
    try {{
        if (!{var_name}.{field1}) {{
            throw new Error('{field1} is required');
        }}
        const validated = await validate{entity}({var_name});
        const result = await db.{entity.lower()}.{operation}({{
            {field1}: validated.{field1},
            {field2}: validated.{field2} || null
        }});
        return {{ success: true, data: result }};
    }} catch (error) {{
        console.error('{operation}{entity} failed:', error);
        return {{ success: false, error: error.message }};
    }}
}}""",
                f"""function {operation}{entity}By{field1.capitalize()}({field1}Value) {{
    return new Promise((resolve, reject) => {{
        if (!{field1}Value) {{
            reject(new Error('{field1} cannot be empty'));
        }}
        database.query(
            'SELECT * FROM {entity.lower()}s WHERE {field1} = ?',
            [{field1}Value],
            (err, results) => {{
                if (err) reject(err);
                else resolve(results);
            }}
        );
    }});
}}""",
                f"""router.post('/{entity.lower()}/:{operation}', async (req, res) => {{
    const {{ {field1}, {field2} }} = req.body;

    if (!{field1} || !{field2}) {{
        return res.status(400).json({{
            error: 'Missing required fields: {field1}, {field2}'
        }});
    }}

    try {{
        const {var_name} = await {entity}Service.{operation}({{
            {field1}, {field2},
            userId: req.user.id,
            timestamp: new Date()
        }});

        res.status(200).json({var_name});
    }} catch (error) {{
        res.status(500).json({{ error: error.message }});
    }}
}}""",
                f"""const {operation}{entity} = ({{ {field1}, {field2}, onSuccess, onError }}) => {{
    const [{var_name}, set{var_name.capitalize()}] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {{
        if ({field1} && {field2}) {{
            setLoading(true);
            api.{operation}{entity}({{ {field1}, {field2} }})
                .then(response => {{
                    set{var_name.capitalize()}(response.data);
                    onSuccess && onSuccess(response.data);
                }})
                .catch(error => {{
                    onError && onError(error);
                }})
                .finally(() => setLoading(false));
        }}
    }}, [{field1}, {field2}]);

    return {{ {var_name}, loading }};
}}""",
                f"""class {entity}Manager {{
    constructor(database) {{
        this.db = database;
        this.cache = new Map();
    }}

    async {operation}{entity}({var_name}) {{
        const cacheKey = {var_name}.{field1} + '-' + {var_name}.{field2};

        if (this.cache.has(cacheKey)) {{
            return this.cache.get(cacheKey);
        }}

        const result = await this.db.{operation}('{entity.lower()}s', {{
            where: {{ {field1}: {var_name}.{field1} }},
            data: {{ {field2}: {var_name}.{field2} }}
        }});

        this.cache.set(cacheKey, result);
        return result;
    }}
}}"""
            ]

            code = random.choice(patterns)
            explanations = [
                f"Asynchronous function to {operation} {entity.lower()} with {field1} validation and error handling",
                f"Promise-based {operation} operation for {entity} filtered by {field1} field",
                f"Express.js route handler for {operation} operation on {entity} resource with request validation",
                f"React hook for {operation} operation on {entity} with {field1} and {field2} parameters",
                f"Class method to {operation} {entity} with caching mechanism based on {field1} and {field2}"
            ]

            samples.append({
                'language': 'javascript',
                'code': code,
                'explanation': random.choice(explanations)
            })

        return samples

    def generate_java(self, count=1000):
        samples = []
        for i in range(count):
            entity = random.choice(self.entities)
            field1 = random.choice(self.fields)
            field2 = random.choice(self.fields)
            operation = random.choice(self.operations)

            patterns = [
                f"""@RestController
@RequestMapping("/api/v1/{entity.lower()}")
public class {entity}Controller {{

    @Autowired
    private {entity}Service service;

    @PostMapping("/{operation}")
    public ResponseEntity<{entity}Response> {operation}{entity}(
            @Valid @RequestBody {entity}Request request,
            @RequestHeader("Authorization") String token) {{

        try {{
            validationService.validate(request);
            {entity} result = service.{operation}(
                request.get{field1.capitalize()}(),
                request.get{field2.capitalize()}(),
                extractUserId(token)
            );

            return ResponseEntity.ok({entity}Response.from(result));
        }} catch (ValidationException e) {{
            return ResponseEntity.badRequest()
                .body({entity}Response.error(e.getMessage()));
        }}
    }}
}}""",
                f"""@Repository
public interface {entity}Repository extends JpaRepository<{entity}, Long> {{

    @Query("SELECT e FROM {entity} e WHERE e.{field1} = :value1 AND e.{field2} = :value2")
    Optional<{entity}> {operation}By{field1.capitalize()}And{field2.capitalize()}(
        @Param("value1") String value1,
        @Param("value2") String value2
    );

    @Modifying
    @Transactional
    @Query("UPDATE {entity} e SET e.{field2} = :newValue WHERE e.{field1} = :identifier")
    int {operation}{entity}Field(
        @Param("identifier") String identifier,
        @Param("newValue") String newValue
    );
}}""",
                f"""@Service
@Transactional
public class {entity}ServiceImpl implements {entity}Service {{

    private final {entity}Repository repository;
    private final CacheManager cacheManager;
    private final EventPublisher eventPublisher;

    @Override
    @Cacheable(value = "{entity.lower()}-cache", key = "#id")
    public {entity}DTO {operation}{entity}(Long id, UpdateRequest request) {{
        log.info("{operation} {entity} with id: {{}}", id);

        {entity} entity = repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("{entity} not found"));

        entity.set{field1.capitalize()}(request.get{field1.capitalize()}());
        entity.set{field2.capitalize()}(request.get{field2.capitalize()}());
        entity.setUpdatedAt(LocalDateTime.now());

        {entity} saved = repository.save(entity);

        eventPublisher.publishEvent(new {entity}UpdatedEvent(saved));

        return {entity}Mapper.toDTO(saved);
    }}
}}""",
                f"""@Component
public class {entity}Validator {{

    public ValidationResult validate{entity}({entity} entity) {{
        List<String> errors = new ArrayList<>();

        if (entity.get{field1.capitalize()}() == null ||
            entity.get{field1.capitalize()}().isEmpty()) {{
            errors.add("{field1} is required");
        }}

        if (entity.get{field2.capitalize()}() != null) {{
            if (!isValid{field2.capitalize()}(entity.get{field2.capitalize()}())) {{
                errors.add("{field2} format is invalid");
            }}
        }}

        if (!errors.isEmpty()) {{
            return ValidationResult.failure(errors);
        }}

        return ValidationResult.success();
    }}
}}"""
            ]

            code = random.choice(patterns)

            explanations = [
                f"Spring Boot REST controller for {operation} operation on {entity} with validation and error handling",
                f"JPA repository interface for {operation} operations on {entity} entity with custom queries",
                f"Service implementation for {operation} {entity} with caching and event publishing",
                f"Validation component for {entity} entity checking {field1} and {field2} fields"
            ]

            samples.append({
                'language': 'java',
                'code': code,
                'explanation': random.choice(explanations)
            })

        return samples

    def generate_sql(self, count=1000):
        samples = []
        for i in range(count):
            entity = random.choice(self.entities)
            entity2 = random.choice(self.entities)
            field1 = random.choice(self.fields)
            field2 = random.choice(self.fields)
            field3 = random.choice(self.fields)
            operation = random.choice(['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'MERGE'])

            patterns = [
                f"""WITH {entity}Summary AS (
    SELECT
        {field1},
        {field2},
        COUNT(*) as total_count,
        AVG(CAST({field3} AS DECIMAL(10,2))) as avg_{field3}
    FROM {entity.lower()}s
    WHERE created_at >= DATEADD(day, -30, GETDATE())
        AND status = 'active'
    GROUP BY {field1}, {field2}
    HAVING COUNT(*) > 5
)
SELECT
    s.*,
    e.{field3},
    RANK() OVER (PARTITION BY s.{field1} ORDER BY s.total_count DESC) as rank_position
FROM {entity}Summary s
INNER JOIN {entity.lower()}s e ON s.{field1} = e.{field1}
ORDER BY s.avg_{field3} DESC;""",
                f"""MERGE {entity.lower()}s AS target
USING (
    SELECT
        @{field1} as {field1},
        @{field2} as {field2},
        @{field3} as {field3}
) AS source
ON target.{field1} = source.{field1}
WHEN MATCHED THEN
    UPDATE SET
        {field2} = source.{field2},
        {field3} = source.{field3},
        updated_at = GETDATE()
WHEN NOT MATCHED THEN
    INSERT ({field1}, {field2}, {field3}, created_at)
    VALUES (source.{field1}, source.{field2}, source.{field3}, GETDATE())
OUTPUT
    $action as action,
    inserted.{field1},
    deleted.{field2} as old_{field2},
    inserted.{field2} as new_{field2};""",
                f"""SELECT
    {field1},
    {field2},
    {field3},
    LAG({field2}) OVER (PARTITION BY {field1} ORDER BY created_at) as prev_{field2},
    LEAD({field2}) OVER (PARTITION BY {field1} ORDER BY created_at) as next_{field2},
    SUM({field3}) OVER (PARTITION BY {field1} ORDER BY created_at
                        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) as rolling_sum,
    DENSE_RANK() OVER (ORDER BY {field3} DESC) as {field3}_rank
FROM {entity.lower()}s
WHERE {field1} IN (
    SELECT DISTINCT {field1}
    FROM {entity2.lower()}s
    WHERE status = 'active'
);""",

                f"""WITH RECURSIVE {entity}Hierarchy AS (
    -- Anchor member
    SELECT
        {field1},
        {field2},
        {field3},
        0 as level,
        CAST({field1} AS VARCHAR(MAX)) as path
    FROM {entity.lower()}s
    WHERE parent_{field1} IS NULL

    UNION ALL

    -- Recursive member
    SELECT
        e.{field1},
        e.{field2},
        e.{field3},
        h.level + 1,
        h.path + '/' + CAST(e.{field1} AS VARCHAR(MAX))
    FROM {entity.lower()}s e
    INNER JOIN {entity}Hierarchy h ON e.parent_{field1} = h.{field1}
    WHERE h.level < 10
)
SELECT * FROM {entity}Hierarchy
ORDER BY path;""",

                f"""UPDATE e1
SET
    e1.{field2} = e2.calculated_{field2},
    e1.{field3} = CASE
        WHEN e2.category = 'premium' THEN e2.{field3} * 1.2
        WHEN e2.category = 'standard' THEN e2.{field3}
        ELSE e2.{field3} * 0.9
    END,
    e1.updated_at = GETDATE(),
    e1.updated_by = SYSTEM_USER
FROM {entity.lower()}s e1
INNER JOIN (
    SELECT
        {field1},
        MAX({field2}) as calculated_{field2},
        AVG({field3}) as {field3},
        category
    FROM {entity2.lower()}s
    GROUP BY {field1}, category
) e2 ON e1.{field1} = e2.{field1}
WHERE e1.status = 'pending'
    AND e1.created_at < DATEADD(hour, -24, GETDATE());"""
            ]

            code = random.choice(patterns)

            explanations = [
                f"CTE-based query to aggregate {entity} data by {field1} and {field2} with ranking",
                f"MERGE statement for upsert operation on {entity} table based on {field1}",
                f"Window function query analyzing {entity} records with lag/lead and rolling calculations",
                f"Recursive CTE to traverse {entity} hierarchy with level tracking",
                f"Complex UPDATE joining {entity} with aggregated {entity2} data applying conditional logic"
            ]

            samples.append({
                'language': 'sql',
                'code': code,
                'explanation': random.choice(explanations)
            })

        return samples

    def generate_dataset(self, train_size=40000, val_size=8000, test_size=2000):
        print(f"Generating diverse dataset with {train_size + val_size + test_size} total samples...")

        js_train = self.generate_javascript(train_size // 3)
        java_train = self.generate_java(train_size // 3)
        sql_train = self.generate_sql(train_size // 3 + train_size % 3)

        js_val = self.generate_javascript(val_size // 3)
        java_val = self.generate_java(val_size // 3)
        sql_val = self.generate_sql(val_size // 3 + val_size % 3)

        js_test = self.generate_javascript(test_size // 3)
        java_test = self.generate_java(test_size // 3)
        sql_test = self.generate_sql(test_size // 3 + test_size % 3)

        train_data = js_train + java_train + sql_train
        val_data = js_val + java_val + sql_val
        test_data = js_test + java_test + sql_test

        random.shuffle(train_data)
        random.shuffle(val_data)
        random.shuffle(test_data)

        return train_data, val_data, test_data

generator = ImprovedDataGenerator()
train_data, val_data, test_data = generator.generate_dataset(
    train_size=40000,
    val_size=8000,
    test_size=2000
)

print(f"✅ Generated {len(train_data)} training samples")
print(f"✅ Generated {len(val_data)} validation samples")
print(f"✅ Generated {len(test_data)} test samples")

class BetterTokenizer:
    def __init__(self):
        self.word_to_id = {'<pad>': 0, '<unk>': 1, '<sos>': 2, '<eos>': 3}
        self.id_to_word = {v: k for k, v in self.word_to_id.items()}
        self.vocab_size = 4

    def fit(self, texts, max_vocab=10000):
        from collections import Counter

        word_counts = Counter()

        for text in texts:
            tokens = text.lower()
            for delimiter in ['\n', '(', ')', '{', '}', '[', ']', ';', ',', '.', ':', '=', '+', '-', '*', '/', '<', '>', '!', '?', '@', '#', '$', '%', '&', '|']:
                tokens = tokens.replace(delimiter, f' {delimiter} ')
            tokens = tokens.split()
            word_counts.update(tokens)

        most_common = word_counts.most_common(max_vocab - len(self.word_to_id))

        for word, count in most_common:
            if word not in self.word_to_id:
                self.word_to_id[word] = self.vocab_size
                self.id_to_word[self.vocab_size] = word
                self.vocab_size += 1

        print(f" Vocabulary size: {self.vocab_size}")
        print(f" Total unique tokens: {len(word_counts)}")
        print(f" Vocabulary coverage: {(self.vocab_size / min(len(word_counts), max_vocab)) * 100:.1f}%")

        return self

    def encode(self, text, max_length=256): 
        tokens = text.lower()
        for delimiter in ['\n', '(', ')', '{', '}', '[', ']', ';', ',', '.', ':', '=', '+', '-', '*', '/', '<', '>', '!', '?', '@', '#', '$', '%', '&', '|']:
            tokens = tokens.replace(delimiter, f' {delimiter} ')
        tokens = tokens.split()

        ids = [self.word_to_id.get(token, 1) for token in tokens[:max_length-2]]
        ids = [2] + ids + [3]

        if len(ids) < max_length:
            ids += [0] * (max_length - len(ids))

        return ids[:max_length]

    def decode(self, ids):
        tokens = [self.id_to_word.get(id, '<unk>') for id in ids]
        tokens = [t for t in tokens if t not in ['<pad>', '<sos>', '<eos>']]
        return ' '.join(tokens)

all_texts = []
for item in train_data + val_data:
    all_texts.append(item['code'])
    all_texts.append(item['explanation'])

tokenizer = BetterTokenizer()
tokenizer.fit(all_texts, max_vocab=10000)

class OptimizedTransformer(nn.Module):
    def __init__(self, vocab_size, d_model=256, n_heads=8, n_layers=4, max_len=256, dropout=0.2):
        super().__init__()
        self.d_model = d_model

        self.token_embedding = nn.Embedding(vocab_size, d_model)
        self.position_embedding = nn.Embedding(max_len, d_model)

        self.layer_norm = nn.LayerNorm(d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=n_heads,
            dim_feedforward=1024,
            dropout=dropout,
            activation='gelu', 
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.output_projection = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)
        self._init_weights()

    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def forward(self, x, mask=None):
        batch_size, seq_len = x.shape
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0).expand(batch_size, -1)
        token_emb = self.token_embedding(x)
        pos_emb = self.position_embedding(positions)

        x = token_emb + pos_emb
        x = self.layer_norm(x)
        x = self.dropout(x)
        x = self.transformer(x, src_key_padding_mask=mask)
        output = self.output_projection(x)

        return output

model = OptimizedTransformer(
    vocab_size=tokenizer.vocab_size,
    d_model=256,     
    n_heads=8,
    n_layers=4,      
    max_len=256,
    dropout=0.2      
).to(device)

total_params = sum(p.numel() for p in model.parameters())
print(f" Model created with {total_params:,} parameters")

class CodeDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=256):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]

        input_text = f"{item['language']}: {item['code']}"
        input_ids = torch.tensor(self.tokenizer.encode(input_text, self.max_length))

        target_ids = torch.tensor(self.tokenizer.encode(item['explanation'], self.max_length))

        input_mask = (input_ids != 0).float()
        target_mask = (target_ids != 0).float()

        return input_ids, target_ids, input_mask, target_mask

train_dataset = CodeDataset(train_data, tokenizer)
val_dataset = CodeDataset(val_data, tokenizer)

batch_size = 32  

train_loader = DataLoader(
    train_dataset,
    batch_size=batch_size,
    shuffle=True,
    num_workers=2 if torch.cuda.is_available() else 0,
    pin_memory=torch.cuda.is_available()
)

val_loader = DataLoader(
    val_dataset,
    batch_size=batch_size,
    shuffle=False,
    num_workers=2 if torch.cuda.is_available() else 0,
    pin_memory=torch.cuda.is_available()
)

print(f"📊 DataLoaders created:")
print(f"   Training batches: {len(train_loader)}")
print(f"   Validation batches: {len(val_loader)}")

class WarmupScheduler:
    def __init__(self, optimizer, warmup_steps, d_model):
        self.optimizer = optimizer
        self.warmup_steps = warmup_steps
        self.d_model = d_model
        self.current_step = 0

    def step(self):
        self.current_step += 1
        lr = self.get_lr()
        for param_group in self.optimizer.param_groups:
            param_group['lr'] = lr

    def get_lr(self):
        if self.current_step < self.warmup_steps:
            return self.d_model**(-0.5) * self.current_step * self.warmup_steps**(-1.5)
        else:
            return self.d_model**(-0.5) * self.current_step**(-0.5)

class LabelSmoothingLoss(nn.Module):
    def __init__(self, vocab_size, padding_idx=0, smoothing=0.1):
        super().__init__()
        self.vocab_size = vocab_size
        self.padding_idx = padding_idx
        self.smoothing = smoothing
        self.confidence = 1.0 - smoothing

    def forward(self, pred, target):
        pred = pred.reshape(-1, self.vocab_size)
        target = target.reshape(-1)

        true_dist = torch.zeros_like(pred)
        true_dist.fill_(self.smoothing / (self.vocab_size - 2))  
        true_dist.scatter_(1, target.unsqueeze(1), self.confidence)
        true_dist[:, self.padding_idx] = 0

        mask = (target != self.padding_idx).float()
        true_dist = true_dist * mask.unsqueeze(1)

        pred = torch.log_softmax(pred, dim=-1)
        loss = torch.sum(-true_dist * pred, dim=-1)

        return loss.mean()

criterion = LabelSmoothingLoss(tokenizer.vocab_size, padding_idx=0, smoothing=0.1)
optimizer = optim.AdamW(model.parameters(), lr=0.0001, weight_decay=0.01, betas=(0.9, 0.98))
scheduler = WarmupScheduler(optimizer, warmup_steps=4000, d_model=256)

def train_epoch(model, loader, criterion, optimizer, scheduler):
    model.train()
    total_loss = 0
    total_tokens = 0

    progress_bar = tqdm(loader, desc="Training")
    for batch_idx, (inputs, targets, input_mask, target_mask) in enumerate(progress_bar):
        inputs = inputs.to(device)
        targets = targets.to(device)
        input_mask = input_mask.to(device)

        outputs = model(inputs, mask=(input_mask == 0)) 
        loss = criterion(outputs, targets)
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        total_loss += loss.item() * inputs.size(0)
        total_tokens += inputs.size(0)
        progress_bar.set_postfix({
            'loss': f'{loss.item():.4f}',
            'lr': f'{scheduler.get_lr():.6f}'
        })

    return total_loss / total_tokens

def validate(model, loader, criterion):
    model.eval()
    total_loss = 0
    total_tokens = 0

    with torch.no_grad():
        for inputs, targets, input_mask, target_mask in tqdm(loader, desc="Validating"):
            inputs = inputs.to(device)
            targets = targets.to(device)
            input_mask = input_mask.to(device)

            outputs = model(inputs, mask=(input_mask == 0))
            loss = criterion(outputs, targets)

            total_loss += loss.item() * inputs.size(0)
            total_tokens += inputs.size(0)

    return total_loss / total_tokens

num_epochs = 50
history = {'train_loss': [], 'val_loss': []}
best_val_loss = float('inf')
patience_counter = 0
patience = 10

print(f"\n Starting training for {num_epochs} epochs")
print("=" * 60)

for epoch in range(num_epochs):
    print(f"\n Epoch {epoch+1}/{num_epochs}")

    train_loss = train_epoch(model, train_loader, criterion, optimizer, scheduler)
    val_loss = validate(model, val_loader, criterion)
    history['train_loss'].append(train_loss)
    history['val_loss'].append(val_loss)
    print(f"📊 Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        torch.save(model.state_dict(), 'best_model.pt')
        print(f" New best model saved (Val Loss: {val_loss:.4f})")
    else:
        patience_counter += 1
        print(f" No improvement for {patience_counter} epochs")

        if patience_counter >= patience:
            print(f"\n Early stopping at epoch {epoch+1}")
            break

    if (epoch + 1) % 5 == 0:
        improvement = ((history['val_loss'][0] - best_val_loss) / history['val_loss'][0]) * 100
        print(f"\n Progress: {improvement:.1f}% improvement from start")

print(f"\n Training complete!")
print(f"Best validation loss: {best_val_loss:.4f}")
model.load_state_dict(torch.load('best_model.pt'))

final_train_loss = history['train_loss'][-1]
final_val_loss = history['val_loss'][-1]
improvement = ((history['val_loss'][0] - best_val_loss) / history['val_loss'][0]) * 100

print("\n" + "=" * 60)
print(" FINAL RESULTS")
print("=" * 60)
print(f"Model Parameters: {total_params:,}")
print(f"Vocabulary Size: {tokenizer.vocab_size:,}")
print(f"Dataset Size: 50,000 samples")
print(f"Epochs Trained: {len(history['train_loss'])}")
print(f"Best Val Loss: {best_val_loss:.4f}")
print(f"Improvement: {improvement:.1f}%")
print("=" * 60)